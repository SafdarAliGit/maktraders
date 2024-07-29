from decimal import Decimal

import frappe
from frappe import _


def execute(filters=None):
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    columns = [
        {
            "label": _("Payment Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Inv. Date"),
            "fieldname": "inv_date",
            "fieldtype": "Date",
            "width": 100
        },
        {
            "label": _("Inv. #"),
            "fieldname": "inv_no",
            "fieldtype": "Link",
            "width": 120,
            "options": "Sales Invoice"
        },
        {
            "label": _("Sale Rep"),
            "fieldname": "sale_rep",
            "fieldtype": "Link",
            "width": 120,
            "options": "Sale Rep"
        },

        {
            "label": _("Party"),
            "fieldname": "party",
            "fieldtype": "Link",
            "width": 120,
            "options": "Customer"
        },

        {
            "label": _("Total Amount"),
            "fieldname": "total_amount",
            "fieldtype": "Float",
            "width": 120
        },
        {
            "label": _("Paid Amount"),
            "fieldname": "paid_amount",
            "fieldtype": "Float",
            "width": 120
        }
    ]

    return columns


def get_conditions(filters):
    conditions = []
    if filters.get("from_date"):
        conditions.append("pe.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append("pe.posting_date <= %(to_date)s")
    if filters.get("sale_rep"):
        conditions.append("si.sale_rep_name = %(sale_rep)s")

    # Join conditions with space and add an optional space before the first condition
    return " AND ".join(conditions) if conditions else ""


def get_data(filters):
    conditions = get_conditions(filters)

    # Base query
    query = f"""
    SELECT 
        pe.posting_date,
        si.posting_date AS inv_date,
        pei.reference_name AS inv_no,
        si.sale_rep_name AS sale_rep,
        pe.party AS party,
        pei.total_amount,
        pe.paid_amount

    FROM `tabPayment Entry` AS pe
    LEFT JOIN `tabPayment Entry Reference` AS pei ON pe.name = pei.parent
    LEFT JOIN `tabSales Invoice` AS si ON pei.reference_name = si.name 
    WHERE
        pei.reference_doctype = 'Sales Invoice'
        AND si.docstatus = 1
        AND pe.payment_type = 'Receive'
    """

    if conditions:
        query += f" AND {conditions}"

    # Execute query and fetch results
    result = frappe.db.sql(query, filters, as_dict=1)

    return result

