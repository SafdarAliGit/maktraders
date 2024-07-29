frappe.query_reports["Sales Rep Receovery Report"] = {
    "filters": [

        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "width": "80",
            "reqd": 1,
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "width": "80",
            "reqd": 1,
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "sale_rep",
            "label": __("Sale Rep"),
            "fieldtype": "Link",
            "width": "80",
            "options": "Sale Rep"
        },

    ]
};

