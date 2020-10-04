# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	columns, data = ["Item Code:Link/Item:120","Item Name:Data:150","Total Qty:Float:100","Total Sales:Currency:200"], []
	conditions = ""
	if filters.get('item_group'):
		conditions  = """ AND d.item_group = "{}" """.format(filters.get('item_group'))
	if filters.get('customer'):
		conditions  = "{} AND p.customer = '{}'".format(conditions,filters.get('customer'))
	if filters.get('customer_group'):
		conditions  = "{} AND p.customer_group = '{}'".format(conditions,filters.get('customer_group'))
	data = frappe.db.sql("""select d.item_code,d.item_name, sum(d.qty) , sum(d.base_amount) as 'total' from `tabSales Invoice Item` d
					join `tabSales Invoice` p on d.parent = p.name
					where p.docstatus=1 and p.is_return=0 and (p.posting_date between "{}" and "{}") {}
					group by d.item_code
                                """.format(filters.get('from_date'),filters.get('to_date'),conditions),as_list=1)
	return columns, data
