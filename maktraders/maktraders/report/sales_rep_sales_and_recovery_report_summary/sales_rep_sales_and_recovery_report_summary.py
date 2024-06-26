# my_custom_app.my_custom_app.report.daily_activity_report.daily_activity_report.py
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
            "label": "<b>Rep Name</b>",
            "fieldname": "sale_rep_name",
            "fieldtype": "Data",
            "width": 120
        },

        {
            "label": "<b>Invoiced Amount</b>",
            "fieldname": "grand_total",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "<b>Return Amount</b>",
            "fieldname": "return_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "<b>Paid Amount</b>",
            "fieldname": "paid_amount",
            "fieldtype": "Currency",
            "width": 120
        },
        {
            "label": "<b>Outstanding</b>",
            "fieldname": "outstanding_amount",
            "fieldtype": "Currency",
            "width": 120
        }

    ]
    return columns


def get_conditions(filters, doctype):
    conditions = []
    if filters.get("from_date"):
        conditions.append(f"`{doctype}`.posting_date >= %(from_date)s")
    if filters.get("to_date"):
        conditions.append(f"`{doctype}`.posting_date <= %(to_date)s")
    return " AND ".join(conditions)


def get_data(filters):
    data = []
    sales_invoice = """
    SELECT 
        inv.sale_rep_name,
        SUM(CASE WHEN inv.status = "Return" THEN inv.grand_total ELSE 0 END) AS return_amount,
        SUM(COALESCE(inv.grand_total,0)) AS grand_total,
        SUM(COALESCE(inv.grand_total, 0) - COALESCE(inv.outstanding_amount,0)) AS paid_amount,
        SUM(inv.outstanding_amount) AS outstanding_amount

    FROM 
        `tabSales Invoice` AS inv
    WHERE 
        inv.docstatus = 1
        AND {conditions}
    GROUP BY
        inv.sale_rep_name
    ORDER BY 
        inv.sale_rep_name
    """.format(conditions=get_conditions(filters, "inv"))

    sales_invoice_result = frappe.db.sql(sales_invoice, filters, as_dict=1)
    # TO REMOVE DUPLICATES
    # keys_to_check = ['customer']
    # seen_values = []
    #
    # for entry in stock_balance_result:
    #     key_values = tuple(entry[key] for key in keys_to_check)
    #
    #     if key_values in seen_values:
    #         for key in keys_to_check:
    #             entry[key] = None
    #     else:
    #         seen_values.append(key_values)

    # END
    data.extend(sales_invoice_result)
    return data
