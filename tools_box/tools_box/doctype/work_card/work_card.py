# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class WorkCard(Document):
    def validate(self):
        if not self.requested_by:
            if self.ticket_number:
                self.requested_by = get_requested_by(self.ticket_number)

        if not self.employee_name:
            if self.ticket_number:
                self.employee_name = get_employee_name(self.employee_name)

        subtotal = 0
        for item in self.work_card_material_detail:
            if not item.item_name:
                item.item_name = get_item_name(item.item_code)
            subtotal = subtotal + item.total
        self.materials_total = subtotal
        self.work_card_total = self.materials_total + self.labour_fees + self.transport_fare
        self.balance_due_upon_work_completion = self.work_card_total - self.work_advance

        # if self.work_completion_date:
        #	if not 'Helpdesk Admin' in frappe.get_roles():
        #		frappe.throw('Only Helpdesk Admin can complete the Work Card.')
        #	else:
        #		self.status = 'Completed'

        # if self.status == 'Completed':
        #	if not self.work_completion_date:
        #		frappe.throw('Work completion date is not set.')


@frappe.whitelist()
def get_work_card_approver(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
		select u.name, concat(u.first_name, ' ', u.last_name)
		from tabUser u, `tabHas Role` r
		where u.name = r.parent and r.role = 'Deputy' 
		and u.enabled = 1 and u.name like %s
	""", ("%" + txt + "%"))


@frappe.whitelist()
def get_requested_by(ticket_type, ticket_number):

    ticket = frappe.get_doc(ticket_type, ticket_number)
    employee = frappe.get_doc("Employee", ticket.raised_by)

    return employee.name


@frappe.whitelist()
def get_employee_name(ticket_type, ticket_number):
    ticket = frappe.get_doc(ticket_type, ticket_number)
    employee = frappe.get_doc("Employee", ticket.raised_by)

    return employee.employee_name


@frappe.whitelist()
def get_item_name(item_code):
    item = frappe.get_doc("Item", item_code)

    return item.item_name


@frappe.whitelist()
def get_item_description(item_code):
    item = frappe.get_doc("Item", item_code)
    return item.description


@frappe.whitelist()
def get_work_cards(start, end):
    data = frappe.db.sql(
        """select name, work_card_date, proposed_completion_date, work_description, status from `tabWork Card` where ((ifnull(work_card_date, '0000-00-00')!= '0000-00-00') and (work_card_date between %(start)s and %(end)s) or ((ifnull(work_card_date, '0000-00-00')!= '0000-00-00') and proposed_completion_date between %(start)s and %(end)s))""",
        {"start": start, "end": end}, as_dict=True)
    return data

@frappe.whitelist()
def get_work_card_description(item):
    if 'New Work Card' in str(item):
        return None
    data = frappe.db.sql(
        f"""select work_description from `tabWork Card` where name='{item}'""",
        as_dict=True
    )
    return data

@frappe.whitelist()
def make_purchase_order(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.ignore_pricing_rule = 1
        target.reference_doctype="Work Card"
        target.run_method("set_missing_values")
        target.run_method("get_schedule_dates")
        target.run_method("calculate_taxes_and_totals")

    target_doc = get_mapped_doc("Work Card", source_name, {
        "Work Card": {
            "doctype": "Purchase Order",
            "field_map": {
                "vendor": "supplier",
                "work_card_date": "transaction_date",
                "name": "reference_docname"
            }
        },
        "Work Card Material Detail": {
            "doctype": "Purchase Order Item",
            "field_map": {
                "item_code": "item_code",
                "item_name": "item_name",
                "item_description": "description",
                "uom": "stock_uom",
                "no_of_units": "qty",
                "unit_cost": "rate",
                "conversion_factor": 1,
                "total": "amount"
            }
        }
    }, target_doc, set_missing_values)

    return target_doc





@frappe.whitelist()
def make_expense_claim(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.run_method("set_missing_values")
        # set missing values for the child table
        d = target.expenses[0]
        d.description = "%s - %s" % (source.work_description, source.work_card_date)
        d.expense_date = target.posting_date
        d.expense_type = "Machine Installation & Repairs"
        d.sanctioned_amount = source.work_card_total
        d.claim_amount = source.work_card_total
        target.expenses[0] = d

        # remove all unneccessary children
        del target.expenses[1:]

    target_doc = get_mapped_doc("Work Card", source_name, {
        "Work Card": {
            "doctype": "Expense Claim",
            "field_map": {
                "work_card_date": "posting_date",
                "name": "work_card",
                "work_description": "remark",
                "approver": "exp_approver"
            }
        },
        "Work Card Material Detail": {
            "doctype": "Expense Claim Detail",
            "field_map": {
                "work_card_date": "posting_date",
            }
        }

    }, target_doc, set_missing_values)

    return target_doc

@frappe.whitelist()
def make_employee_advance(source_name, target_doc=None):
    def set_missing_values(source, target):
        target.run_method("set_missing_values")
        # set missing values for the child table
        target.purpose = "%s - %s" % (source.work_description, source.work_card_date)
        target.advance_amount = source.work_card_total
        target.ref_doctype = "Work Card"
        target.reference_name = source.name

    target_doc = get_mapped_doc("Work Card", source_name, {
        "Work Card": {
            "doctype": "Employee Advance",
            "field_map": {
                "work_card_date": "posting_date",
            }
        },
    }, target_doc, set_missing_values)

    return target_doc
