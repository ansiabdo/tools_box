// Copyright (c) 2016, masonarmani38@gmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Sales By Customer"] = {
	"filters": [{
            fieldname: "from",
            label: __("Report From"),
            fieldtype: "Date",
			reqd:1,
			"default": get_today(),
        },
        {
            fieldname: "to",
            label: __("Report To"),
            fieldtype: "Date",
			reqd:1,
			"default": get_today(),
        },{
            fieldname: "item",
            label: __("Item"),
            fieldtype: "Link",
			options:"Item",
			reqd:0
        }
	]
}
