# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, cint, getdate


def execute(filters=None):
	if not filters: filters = {}

	validate_filters(filters)

	columns = get_columns()
	item_map = get_item_details(filters)
	iwb_map = get_item_warehouse_map(filters)

	data = []
	for (company, item, warehouse) in sorted(iwb_map):
		qty_dict = iwb_map[(company, item, warehouse)]

		data.append([
			item, item_map[item]["item_name"],
			item_map[item]["item_group"],
			item_map[item]["stock_uom"],
			qty_dict.bal_qty,
			qty_dict.val_rate,
			qty_dict.bal_val
		])

	return columns, data


def get_columns():
	"""return columns"""

	columns = [
		_("Item") + ":Link/Item:100",
		_("Item Name") + "::150",
		_("Item Group") + "::150",
		_("Stock UOM") + "::150",
		_("Balance Qty") + ":Float:150",
		_("Valuation Rate") + ":Float:150",
		_("Valuation") + ":Currency:100"
	]

	return columns


def get_conditions(filters):
	conditions = ""
	if filters.get("as_at"):
		conditions += " and sle.posting_date <= '%s'" % frappe.db.escape(filters.get("as_at"))
	else:
		frappe.throw(_("'As At Date' is required"))

	if filters.get('item_group'):
		conditions += " and item.item_group = '%s'" % frappe.db.escape(filters.get("item_group"))

	if filters.get('item'):
		conditions += " and item.item_code = '%s'" % frappe.db.escape(filters.get("item"))

	conditions += " and exists (select name from `tabWarehouse` wh where name like '%finished%' and sle.warehouse = wh.name)"

	return conditions


def get_stock_ledger_entries(filters):
	conditions = get_conditions(filters)

	join_table_query = ""
	if filters.get("item_group"):
		join_table_query = "inner join `tabItem` item on (item.name = sle.item_code)"

	return frappe.db.sql("""
		select
			sle.item_code, warehouse, sle.posting_date, sle.actual_qty, sle.valuation_rate,
			sle.company, sle.voucher_type, sle.qty_after_transaction, sle.stock_value_difference
		from
			`tabStock Ledger Entry` sle force index (posting_sort_index) %s
		where sle.docstatus < 2 %s 
		order by sle.posting_date, sle.posting_time, sle.name""" %
						 (join_table_query, conditions), as_dict=1)


def get_item_warehouse_map(filters):
	iwb_map = {}
	sle = get_stock_ledger_entries(filters)

	for d in sle:
		key = (d.company, d.item_code, d.warehouse)
		if key not in iwb_map:
			iwb_map[key] = frappe._dict({

				"bal_qty": 0.0, "bal_val": 0.0,
				"val_rate": 0.0
			})

		qty_dict = iwb_map[(d.company, d.item_code, d.warehouse)]

		if d.voucher_type == "Stock Reconciliation":
			qty_diff = flt(d.qty_after_transaction) - qty_dict.bal_qty
		else:
			qty_diff = flt(d.actual_qty)

		value_diff = flt(d.stock_value_difference)

		qty_dict.val_rate = d.valuation_rate
		qty_dict.bal_qty += qty_diff
		qty_dict.bal_val += value_diff

	iwb_map = filter_items_with_no_transactions(iwb_map)

	return iwb_map


def filter_items_with_no_transactions(iwb_map):
	for (company, item, warehouse) in sorted(iwb_map):
		qty_dict = iwb_map[(company, item, warehouse)]

		no_transactions = True
		float_precision = cint(frappe.db.get_default("float_precision")) or 3
		for key, val in qty_dict.items():
			val = flt(val, float_precision)
			qty_dict[key] = val
			if key != "val_rate" and val:
				no_transactions = False

		if no_transactions:
			iwb_map.pop((company, item, warehouse))

	return iwb_map


def get_item_details(filters):

	conditions = ''

	if filters.get('item_group'):
		conditions += " and i.item_group = '%s'" % frappe.db.escape(filters.get("item_group"))

	if filters.get('item'):
		conditions += " and i.item_code = '%s'" % frappe.db.escape(filters.get("item"))

	items = frappe.db.sql("""select name, item_name, stock_uom, item_group
		from tabItem i WHERE (1=1) {condition}""".format(condition=conditions), as_dict=1)

	return dict((d.name, d) for d in items)



def validate_filters(filters):
	if not (filters.get("warehouse")):
		sle_count = flt(frappe.db.sql("""select count(name) from `tabStock Ledger Entry`""")[0][0])
		if sle_count > 500000:
			frappe.throw(_("Please set filter based on Item or Warehouse"))
