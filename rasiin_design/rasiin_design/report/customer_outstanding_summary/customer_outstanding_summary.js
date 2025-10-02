// Copyright (c) 2025, Rasiin and contributors
// For license information, please see license.txt

// frappe.query_reports["Customer Outstanding Summary"] = {
// 	"filters": [

// 	]
// };


// customers_outstanding_report.js
frappe.query_reports["Customer Outstanding Summary"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "reqd": 1,
            "default": frappe.defaults.get_user_default("Company")
        },
        {
            "fieldname": "as_on_date",
            "label": __("As On Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today()
        },
        {
            "fieldname": "customer",
            "label": __("Customer"),
            "fieldtype": "Link", 
            "options": "Customer"
        }
    ]
};