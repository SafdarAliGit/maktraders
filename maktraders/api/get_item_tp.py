# sales_invoice_item.py
from __future__ import unicode_literals
import frappe

@frappe.whitelist()
def get_item_tp(item_code):
    """Fetch TP (Trade Price) from Item"""
    if not item_code:
        return 0
        
    tp = frappe.db.get_value("Item", item_code, "tp") or 0
    return flt(tp)