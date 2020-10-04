// Copyright (c) 2016, Anthony Emmanuel https://github.com/mymi14s and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Material Request Items Report"] = {
    "filters": [
        {
            "fieldname": "from",
            "label": __("From"),
            "fieldtype": "Date",
            "width": "80",
            "reqd": 1,
            "default": frappe.datetime.month_start()
        },
        {
            "fieldname": "to",
            "label": __("To"),
            "fieldtype": "Date",
            "width": "80",
            "reqd": 1,
            "default": frappe.datetime.month_end()
        }

    ]
}
