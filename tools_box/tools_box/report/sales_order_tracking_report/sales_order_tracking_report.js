// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales Order Tracking Report"] = {
    "filters": [
        {
            "fieldname": "opened_from",
            "label": __("Opened From"),
            "fieldtype": "Date",
            "width": "80",
            "reqd": 1,
            "default": dateutil.week_start()
        },
        {
            "fieldname": "opened_to",
            "label": __("Opened To"),
            "fieldtype": "Date",
            "width": "80",
            "reqd": 1,
            "default": dateutil.week_end()
        }
    ]

};
