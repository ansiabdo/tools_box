# Copyright (c) 2020, mymi14s@hotmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _

import frappe

def execute(filters=None):
	columns, data = get_column(), get_data(filters)
	return columns, data

def get_data(filters):
    conditions = ""
    if filters.get('opened_from') and filters.get('opened_to'):
        conditions += " '{0} 00:00:00.000000' AND '{1} 23:59:59.999999'".format(
            filters.get("opened_from"), filters.get('opened_to'))


    # open_date, matter, client , status , practice_area , close_date
    sql = f"""SELECT `tabSales Order`.customer, `tabSales Order`.name as sales_order,  `tabSales Invoice Item`.delivery_note, `tabSales Invoice Item`.parent as sales_invoice, 
		`tabSales Order`.grand_total, `tabSales Order`.status as order_status, `tabSales Invoice`.status as inv_status, `tabSales Order`.comment FROM `tabSales Order` INNER JOIN `tabSales Invoice Item` ON 
		`tabSales Order`.name=`tabSales Invoice Item`.sales_order INNER JOIN `tabSales Invoice` ON `tabSales Invoice Item`.parent=`tabSales Invoice`.name 
		WHERE `tabSales Order`.creation between {conditions} GROUP BY delivery_note ORDER BY `tabSales Order`.customer;"""
    data = frappe.db.sql(sql)
    return data


def get_column():
    # ["Link:Link/Accident:150", "Data:Data:200", "Currency:Currency:100", "Float:Float:100"]
    return [
       # _("Open Date") + ":Data:100",
        "Customer:Link/Customer:200",
        "Sales Order:Link/Sales Order:150",
        "Delivery Note:Link/Delivery Note:150",
        "Sales Invoice:Link/Sales Invoice:150",
        "Amount:Currency/curency:120",
        "Ord Status:Data:120",
        "Inv Status:Data:120",
        "Comment:Data:200"
    ]
