# -*- coding: utf-8 -*-
# Copyright (c) 2017, masonarmani38@gmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc
from erpnext import get_default_company


class OvertimeSheet(Document):
    def validate(self):
        overtime_sheet = frappe.db.sql("""select name from `tabOvertime Sheet` where overtime_request=\"%s\" and name != '%s'"""
                            % (self.overtime_request, self.name))
        if overtime_sheet:
            frappe.throw("Sorry, Overtime Request %s is already in use." % self.overtime_request)



@frappe.whitelist()
def make_employee_advance(docname):
    def check_ea_exists():
        frappe.errprint("""select name from `tabEmployee Advance` where reference_name = \"%s\" """ % overtime.name)
        ea = frappe.db.sql("""select name from `tabEmployee Advance` where reference_name = \"%s\" """, overtime.name)
        return ea[0][0] if ea else ""

    overtime = frappe.get_doc("Overtime Sheet", docname)
    if check_ea_exists():
        frappe.throw(_("Employee Advance {0} already exists for the Overtime sheet").format(ea))

    total = 0
    for i in overtime.overtime_information:
        total += i.amount

    emp_advance = frappe.new_doc("Employee Advance")
    emp_advance.employee = overtime.raised_by
    emp_advance.ref_doctype = "Overtime Sheet"
    emp_advance.reference_name = overtime.name
    emp_advance.advance_amount = total
    emp_advance.purpose = _("Overtime payment for {0} between {1} and {2}").format(overtime.name, overtime.start_time,
                                                                                overtime.end_time)

    return emp_advance.as_dict()


@frappe.whitelist()
def make_expense_claim_new(docname):
    def check_exp_claim_exists():
        exp = frappe.db.sql("""select name from `tabExpense Claim` where overtime_request='%s'""", overtime.name)
        return exp[0][0] if exp else ""

    overtime = frappe.get_doc("Overtime Sheet", docname)
    exp_claim = check_exp_claim_exists()
    if exp_claim:
        frappe.throw(_("Expense Claim {0} already exists for the Overtime sheet").format(exp_claim))

    total = 0
    for i in overtime.overtime_information:
        total += i.amount

    exp_claim = frappe.new_doc("Expense Claim")
    exp_claim.employee = overtime.raised_by
    exp_claim.overtime = overtime.name
    exp_claim.remark = _("Overtime payment for {0} between {1} and {2}").format(overtime.name, overtime.start_time,
                                                                                overtime.end_time)
    exp_claim.append("expenses", {
        "expense_date": overtime.date,
        "description": _("Overtime payment for {0} between {1} and {2}").format(overtime.name, overtime.start_time,
                                                                                overtime.end_time),
        "expense_type": "Overtime",
        "claim_amount": total,
        "sanctioned_amount": total
    })
    return exp_claim.as_dict()


@frappe.whitelist()
def make_expense_claim_from_list(docnames):
    docnames = [x for x in str.split(str(docnames),"~~") if x != "" ]

    def check_exp_claim_exists(docname):
        exp = frappe.db.sql("""select name from `tabExpense Claim` where overtime=%s""", docname)
        return exp[0][0] if exp else ""



    for docname in docnames:
        overtime = frappe.get_doc("Overtime Sheet", docname)
        exp_claim = check_exp_claim_exists(overtime.name)
        if exp_claim:
            frappe.throw(_("Expense Claim {0} already exists for the Overtime sheet").format(exp_claim))
        total = 0
        for i in overtime.overtime_information:
            total += i.amount


    exp_claim = check_exp_claim_exists(overtime.name)
    if exp_claim:
        frappe.throw(_("Expense Claim {0} already exists for the Overtime sheet").format(exp_claim))

    total = 0
    for i in overtime.overtime_information:
        total += i.amount

    exp_claim = frappe.new_doc("Expense Claim")
    exp_claim.employee = overtime.raised_by
    exp_claim.overtime = overtime.name
    exp_claim.remark = _("Overtime payment for {0} between {1} and {2}").format(overtime.name, overtime.start_time,
                                                                                overtime.end_time)
    exp_claim.append("expenses", {
        "expense_date": overtime.date,
        "description": _("Overtime payment for {0} between {1} and {2}").format(overtime.name, overtime.start_time,
                                                                                overtime.end_time),
        "expense_type": "Overtime",
        "claim_amount": total,
        "sanctioned_amount": total
    })

    return exp_claim.as_dict()
