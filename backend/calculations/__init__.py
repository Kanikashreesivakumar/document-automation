"""
Calculations module — pure functions with no side effects.
All business calculations for shipment documents live here.
No database access. No imports from other app modules.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional


# ─── Egg / Package Calculations ───────────────────────────────────────────────

def calc_eggs_per_carton(trays_per_carton: int, eggs_per_tray: int) -> int:
    """Total eggs that fit in one carton."""
    return trays_per_carton * eggs_per_tray


def calc_total_eggs(cartons: int, eggs_per_carton: int) -> int:
    """Total eggs across all cartons."""
    return cartons * eggs_per_carton


# ─── Pricing Calculations ──────────────────────────────────────────────────────

def calc_amount_usd(total_eggs: int, rate_per_egg_usd: float) -> float:
    """Total invoice amount in USD."""
    result = Decimal(str(total_eggs)) * Decimal(str(rate_per_egg_usd))
    return float(result.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


# ─── Weight Calculations ───────────────────────────────────────────────────────

def calc_net_weight(cartons: int, net_weight_per_carton: float) -> float:
    """Total net weight in KGS."""
    result = Decimal(str(cartons)) * Decimal(str(net_weight_per_carton))
    return float(result.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


def calc_gross_weight(cartons: int, gross_weight_per_carton: float) -> float:
    """Total gross weight in KGS."""
    result = Decimal(str(cartons)) * Decimal(str(gross_weight_per_carton))
    return float(result.quantize(Decimal("0.001"), rounding=ROUND_HALF_UP))


# ─── Amount in Words ───────────────────────────────────────────────────────────

_ONES = [
    "", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT", "NINE",
    "TEN", "ELEVEN", "TWELVE", "THIRTEEN", "FOURTEEN", "FIFTEEN", "SIXTEEN",
    "SEVENTEEN", "EIGHTEEN", "NINETEEN",
]
_TENS = [
    "", "", "TWENTY", "THIRTY", "FORTY", "FIFTY",
    "SIXTY", "SEVENTY", "EIGHTY", "NINETY",
]


def _words_under_thousand(n: int) -> str:
    if n == 0:
        return ""
    if n < 20:
        return _ONES[n]
    if n < 100:
        tens, ones = divmod(n, 10)
        return _TENS[tens] + (" " + _ONES[ones] if ones else "")
    hundreds, remainder = divmod(n, 100)
    return _ONES[hundreds] + " HUNDRED" + (" AND " + _words_under_thousand(remainder) if remainder else "")


def _integer_to_words(n: int) -> str:
    if n == 0:
        return "ZERO"
    parts = []
    billions, n = divmod(n, 1_000_000_000)
    millions, n = divmod(n, 1_000_000)
    thousands, remainder = divmod(n, 1_000)
    if billions:
        parts.append(_words_under_thousand(billions) + " BILLION")
    if millions:
        parts.append(_words_under_thousand(millions) + " MILLION")
    if thousands:
        parts.append(_words_under_thousand(thousands) + " THOUSAND")
    if remainder:
        parts.append(_words_under_thousand(remainder))
    return " ".join(parts)


def calc_amount_in_words(amount_usd: float) -> str:
    """
    Convert a USD amount to words.
    e.g. 47250.00 → 'US DOLLARS FORTY SEVEN THOUSAND TWO HUNDRED AND FIFTY ONLY'
    """
    if amount_usd <= 0:
        return ""
    amount = Decimal(str(amount_usd)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    dollars = int(amount)
    cents = int((amount - dollars) * 100)
    result = "US DOLLARS " + _integer_to_words(dollars)
    if cents:
        result += " AND CENTS " + _integer_to_words(cents)
    result += " ONLY"
    return result


# ─── Convenience: compute all derived fields at once ──────────────────────────

def compute_all(
    cartons: int,
    trays_per_carton: int,
    eggs_per_tray: int,
    rate_per_egg_usd: float,
    net_weight_per_carton: float,
    gross_weight_per_carton: float,
) -> dict:
    """
    Single entry point used by the service layer.
    Returns a dict of all auto-calculated values.
    """
    eggs_per_carton = calc_eggs_per_carton(trays_per_carton, eggs_per_tray)
    total_eggs = calc_total_eggs(cartons, eggs_per_carton)
    amount_usd = calc_amount_usd(total_eggs, rate_per_egg_usd)
    net_weight = calc_net_weight(cartons, net_weight_per_carton)
    gross_weight = calc_gross_weight(cartons, gross_weight_per_carton)
    amount_in_words = calc_amount_in_words(amount_usd)

    return {
        "eggs_per_carton": eggs_per_carton,
        "total_eggs": total_eggs,
        "amount_usd": amount_usd,
        "amount_in_words": amount_in_words,
        "net_weight": net_weight,
        "gross_weight": gross_weight,
    }
