# Copyright (c) 2019, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe


def execute_0(filters=None):
	if not filters: filters ={}
	columns = [
		"Item:Link/Item:300",
		"Item Group:Link/Item Group:140",
		"Customer:Link/Customer:200",
		"Qty:Float:50",
		"Amount:Currency:150"
	]

	conditions = ""
	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"
	if filters.get("customer"):
		conditions += " AND si.customer = %(customer)s"
	if filters.get("item"):
		conditions += " AND sii.item_code = %(item)s"

	if filters.get("customer_group"):
		conditions += """ AND c.customer_group = %(customer_group)s """
	if filters.get("item_group"):
		conditions += """ AND i.item_group = %(item_group)s """

	query = """SELECT sii.item_name, i.item_group, si.posting_date,si.name,si.customer,
		SUM(sii.qty) qty ,SUM(sii.amount) amount FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` sii 
		ON(sii.parent = si.name)  INNER JOIN `tabCustomer` c ON(si.customer=c.name) INNER JOIN `tabItem` i 
		ON(i.name=sii.item_code) WHERE si.is_return =0 AND si.docstatus = 1 %s GROUP BY sii.item_code ORDER BY sii.item_name,si.posting_date """ % conditions

	frappe.errprint(query.format(**filters))
	data = frappe.db.sql(query ,filters)
	return columns, data




def execute(filters=None):
	if not filters: filters ={}
	columns = [
		"Item:Link/Item:300",
		"Item Group:Link/Item Group:140",
		"Qty:Float:100",
		"Amount With Discount:Currency:100",
		"Amount Without Discount:Currency:100",
		"Last Customer Territory:Link/Territory:150"
	]

	conditions = ""
	if filters.get("from_date"):
		conditions += " AND si.posting_date >= %(from_date)s"
	if filters.get("to_date"):
		conditions += " AND si.posting_date <= %(to_date)s"
	if filters.get("customer"):
		conditions += " AND si.customer = %(customer)s"
	if filters.get("item"):
		conditions += " AND sii.item_code = %(item)s"
	if filters.get("item_group"):
		conditions += " AND i.item_group = %(item_group)s"
	if filters.get("customer_group"):
		conditions += " AND c.customer_group = %(customer_group)s"
	if filters.get("territory"):
		conditions += " AND c.territory = %(territory)s"


	data = frappe.db.sql("""SELECT sii.item_name, i.item_group, 
		SUM(sii.qty),SUM(sii.net_amount) net,SUM(sii.amount) amount,c.territory FROM `tabSales Invoice` si INNER JOIN `tabSales Invoice Item` sii 
		ON(sii.parent = si.name) INNER JOIN `tabCustomer` c ON(si.customer=c.name) INNER JOIN `tabItem` i 
		ON(i.name=sii.item_code)WHERE si.docstatus = 1%s GROUP BY i.name ORDER BY qty""" % conditions,filters)
	return columns, data