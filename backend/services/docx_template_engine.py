"""Reusable DOCX template helpers.

The helpers in this module only replace text in existing paragraphs/runs and
optionally inject a header image. They do not rebuild layouts, sections, or
paragraph structure.
"""
from __future__ import annotations

from pathlib import Path
from typing import Mapping

from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph
from docx.table import Table, _Cell
from docx.shared import Inches, Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH


W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _iter_paragraphs(container):
    # Use XPath to find all w:p elements in the container's XML.
    # This ensures we cover paragraphs inside tables, text boxes (w:txbxContent),
    # shapes, and headers/footers reliably.
    if hasattr(container, "_element"):
        for p_elem in container._element.xpath(".//w:p"):
            # Provide the container as the parent so Paragraph can access .part if needed
            yield Paragraph(p_elem, container)
    else:
        # Fallback for containers without _element (rare)
        if hasattr(container, "paragraphs"):
            for paragraph in container.paragraphs:
                yield paragraph
        if hasattr(container, "tables"):
            for table in container.tables:
                yield from _iter_table_paragraphs(table)


def _iter_table_paragraphs(table: Table):
    for row in table.rows:
        for cell in row.cells:
            yield from _iter_cell_paragraphs(cell)


def _iter_cell_paragraphs(cell: _Cell):
    for paragraph in cell.paragraphs:
        yield paragraph
    for table in cell.tables:
        yield from _iter_table_paragraphs(table)


def _paragraph_text(paragraph: Paragraph) -> str:
    return "".join(run.text for run in paragraph.runs)


def _run_positions(paragraph: Paragraph):
    positions = []
    cursor = 0
    for run in paragraph.runs:
        text = run.text or ""
        start = cursor
        cursor += len(text)
        positions.append((run, start, cursor))
    return positions, cursor


def _replace_span_in_paragraph(paragraph: Paragraph, placeholder: str, replacement: str) -> bool:
    positions, total_length = _run_positions(paragraph)
    if total_length == 0:
        return False

    full_text = _paragraph_text(paragraph)
    index = full_text.find(placeholder)
    if index < 0:
        return False

    end = index + len(placeholder)
    start_run_index = end_run_index = None
    for idx, (_, run_start, run_end) in enumerate(positions):
        if start_run_index is None and run_end > index:
            start_run_index = idx
        if run_end >= end:
            end_run_index = idx
            break

    if start_run_index is None or end_run_index is None:
        return False

    start_run, start_start, _ = positions[start_run_index]
    end_run, _, end_end = positions[end_run_index]
    start_text = start_run.text or ""
    end_text = end_run.text or ""

    prefix = start_text[: max(0, index - start_start)]
    suffix = end_text[max(0, end - positions[end_run_index][1]) :]

    if start_run_index == end_run_index:
        start_run.text = prefix + replacement + suffix
        return True

    start_run.text = prefix + replacement
    for idx in range(start_run_index + 1, end_run_index):
        positions[idx][0].text = ""
    end_run.text = suffix
    return True


def replace_text(document: Document, replacements: Mapping[str, object]) -> None:
    """Replace arbitrary literal strings while preserving run formatting."""
    normalized = {str(old): "" if new is None else str(new) for old, new in replacements.items()}

    def process_container(container):
        for paragraph in _iter_paragraphs(container):
            for old, new in normalized.items():
                if old in _paragraph_text(paragraph):
                    if old in new:
                        _replace_span_in_paragraph(paragraph, old, new)
                    else:
                        while _replace_span_in_paragraph(paragraph, old, new):
                            pass

    process_container(document)
    for section in document.sections:
        process_container(section.header)
        process_container(section.footer)


def replace_placeholders(document: Document, replacements: Mapping[str, object]) -> None:
    """Replace all placeholders in document body, headers, and footers.

    Replacements are applied to runs only; section layout, paragraph formatting,
    tables, and merged cells remain intact.
    """
    normalized = {f"{{{{ {key} }}}}": "" if value is None else str(value) for key, value in replacements.items()}
    replace_text(document, normalized)


def _enable_first_page_header_only(section) -> None:
    """
    Set titlePg on the section so that the first-page header is separate from
    the default (continuation page) header. Then clear the default header so
    that pages 2+ have no header.
    """
    # Enable different first-page header via <w:titlePg/>
    sect_pr = section._sectPr
    title_pg = sect_pr.find(qn("w:titlePg"))
    if title_pg is None:
        title_pg = OxmlElement("w:titlePg")
        sect_pr.insert(0, title_pg)

    # Clear the default (even/odd) header — this is what shows on page 2+
    default_header = section.header
    for p in default_header.paragraphs:
        for run in p.runs:
            run.text = ""
        p.text = ""

    # Also explicitly mark the default header as linked to previous (empty)
    # by removing any content and leaving it empty.
    for p in default_header.paragraphs:
        p._element.clear()
        # Re-add a minimal empty paragraph element so the header stays valid
        pPr = OxmlElement("w:pPr")
        p._element.append(pPr)


def ensure_letterhead_header(document: Document, image_path: str | Path) -> None:
    """
    Insert the company letterhead on the FIRST PAGE ONLY using standard python-docx APIs.

    - The header appears only on page 1.
    - Pages 2+ have an empty header (no logo repeat).
    - The image is centered on the physical page (accounting for asymmetric margins).
    - No image resizing, cropping, or stretching.
    """
    image_path = Path(image_path)
    if not image_path.exists():
        raise FileNotFoundError(f"Header image not found: {image_path}")

    # Image dimensions:
    #   width  = 7.5in, aspect = 3.275 → height ≈ 2.29in
    # Physical centering on 8.5in page:
    #   center start from left page edge = (8.5 - 7.5) / 2 = 0.5in
    # Body content left margin = 0.35in (original from source documents).
    # → indent from content area left edge = 0.5 - 0.35 = 0.15in
    # Using LEFT alignment + left_indent of 0.15in places the image exactly centered
    # on the physical page while leaving body content at its original 0.35in position.
    IMAGE_WIDTH = Inches(7.5)
    # Distance from physical left page edge to where the centered image should start
    PHYSICAL_LEFT_START = Inches(0.5)

    for section in document.sections:
        # ── Page margins ────────────────────────────────────────────────────────
        # Keep original body document margins so tables stay in their source positions.
        # header_distance + image_height = top_margin
        # 0.1in header_distance + 2.29in image height = 2.39in → 2.4in
        section.header_distance = Inches(0.1)
        section.top_margin = Inches(2.4)
        section.bottom_margin = Inches(0.15)
        section.left_margin = Inches(0.35)   # Original body left margin
        section.right_margin = Inches(0)   # Original body right margin

        # ── Enable first-page-only header ──────────────────────────────────────
        _enable_first_page_header_only(section)

        # ── Populate the FIRST-PAGE header ────────────────────────────────────
        first_header = section.first_page_header

        # Completely wipe the first-page header XML and rebuild with a single paragraph.
        # Using p._element.clear() removes ALL child elements including w:drawing nodes
        # (which p.text = "" does NOT remove).
        hdr_el = first_header._element
        # Remove all w:p elements from the header
        for child in list(hdr_el):
            hdr_el.remove(child)

        # Add a fresh paragraph into the header element
        from docx.oxml import OxmlElement as _OE
        p_el = _OE("w:p")
        hdr_el.append(p_el)

        # Access it via python-docx
        paragraph = first_header.paragraphs[0]
        # Use LEFT alignment with a calculated left_indent so the image is physically
        # centered on the page regardless of the section left margin.
        paragraph.alignment = WD_ALIGN_PARAGRAPH.LEFT
        pf = paragraph.paragraph_format
        pf.space_before = Pt(0)
        pf.space_after = Pt(0)
        pf.line_spacing = 1
        # Indent = physical_left_start - section.left_margin
        # = 0.5in - 0.35in = 0.15in
        pf.left_indent = PHYSICAL_LEFT_START - section.left_margin

        run = paragraph.add_run()
        run.add_picture(str(image_path), width=IMAGE_WIDTH)


def fill_docx_template(template_path: str | Path, output_path: str | Path, replacements: Mapping[str, object]) -> None:
    """Load a DOCX template, replace placeholders, and save the filled document."""
    template_path = Path(template_path)
    output_path = Path(output_path)
    document = Document(str(template_path))
    replace_placeholders(document, replacements)
    document.save(str(output_path))