import { z } from "zod";

const strO = () => z.string().optional().or(z.literal(""));

export const proformaInvoiceSchema = z.object({
  po_number: strO(),
  po_date: strO(),
  proforma_invoice_number: strO(),
  buyer_trn: strO(),
  consignee_trn: strO(),
  notify_party: strO(),
  notify_party_address: strO(),
  payment_terms: strO(),
  expiry_date: strO(),
  no_and_kind_of_packages: strO(),
  intermediate_bank_name: strO(),
  intermediate_bank_account_number: strO(),
  intermediate_bank_swift: strO(),
  intermediate_bank_routing_number: strO(),
  correspondent_bank: strO(),
});

export type ProformaInvoiceForm = z.infer<typeof proformaInvoiceSchema>;
