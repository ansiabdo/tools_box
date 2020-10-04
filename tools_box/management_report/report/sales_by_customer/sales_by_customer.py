# Copyright (c) 2013, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

def execute(filters=None):
	conditions = ""
	if filters.get('item'):
		conditions  = " AND d.item_code = '%s'" % filters.get('item')
	columns = ["Customer:Link/Customer:250","Total Sales:Currency:250"]
	data = frappe.db.sql("""select * from (select p.customer , sum(d.base_amount) as 'total' from `tabSales Invoice Item` d 
				join `tabSales Invoice` p on d.parent = p.name 
				where p.docstatus=1 and p.is_return=0 and (p.posting_date between "{}" and "{}") {}
				group by p.customer limit 0,50) temp
				order by temp.total desc
				""".format(filters.get('from'),filters.get('to'),conditions),as_list=1)
	return columns,data
