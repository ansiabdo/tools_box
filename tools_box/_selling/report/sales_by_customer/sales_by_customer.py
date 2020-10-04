# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	conditions = ""
	if filters.get('item'):
		conditions  = " AND item.item_code = '%s'" % filters.get('item')

	if filters.get('to') and filters.get('from'):
		customers = frappe.db.sql(
			"SELECT DISTINCT si.customer, SUM(si.total) amount FROM `tabSales Invoice` si INNER JOIN "
			"`tabSales Invoice Item` sii ON(sii.parent = si.name) INNER  JOIN `tabItem` item ON(item.item_code = sii.item_code)"
			" WHERE si.docstatus = 1 and si.is_return = 0 %s "
			" GROUP BY si.customer ORDER BY amount DESC limit 50 " % conditions, as_dict=1)


		columns, data = get_cols(), []

		top = 1
		for cust in customers:
			cust.update({"rank":top })
			data.append(cust)
			top = top + 1

		return columns, data


def get_cols():
	return [{
		"fieldname": "customer",
		"label": _("Customer Name"),
		"fieldtype": "Data",
		"width": 160
	}, {
		"fieldname": "amount",
		"label": _("Amount"),
		"fieldtype": "Currency",
		"width": 120
	}, {
		"fieldname": "rank",
		"label": "Rank",
		"fieldtype": "Data",
		"width": 100
	}]