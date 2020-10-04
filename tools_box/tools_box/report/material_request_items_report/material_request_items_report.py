# Copyright (c) 2013, masonarmani38@gmail.com, Anthony Emmanuel https://github.com/mymi14s and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _

import frappe


def execute(filters=None):
    return get_column(), get_data(filters)


def get_data(filters):
	data = None
	if filters.get('from') and filters.get('to'):
		conditions = f"'{filters.get('from')} 00:00:00' AND '{filters.get('to')} 23:59:59'"
		data = frappe.db.sql(f"""
			SELECT `tabMaterial Request Item`.item_code, `tabMaterial Request Item`.item_name, sum(`tabMaterial Request Item`.qty),
			`tabMaterial Request Item`.description FROM `tabMaterial Request Item` INNER JOIN `tabMaterial Request` ON
			`tabMaterial Request Item`.parent=`tabMaterial Request`.name WHERE `tabMaterial Request`.creation BETWEEN {conditions}
			AND (`tabMaterial Request`.status='Ordered' OR `tabMaterial Request`.status='Recieved') GROUP BY item_code;
		""")
		return data

def get_column():
    # ["Link:Link/Accident:150", "Data:Data:200", "Currency:Currency:100", "Float:Float:100"]
    return [
        "Item Code:Data:100",
        "Item Name:Data:200",
        "Qty:Data:80",
        "Description:Data:300",
    ]
