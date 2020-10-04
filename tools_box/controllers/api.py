# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _

from frappe.model.utils import get_fetch_values
from frappe.model.mapper import get_mapped_doc
from frappe.utils import cstr, flt, getdate, comma_and, cint, nowdate, add_days


import datetime
from frappe import sendmail


@frappe.whitelist()
def get_active_employees(doctype, txt, searchfield, start, page_len, filters):
    return _get(txt, start, page_len)


def _get(text=None, start=0, page_len=5):
    return frappe.db.sql("""select DISTINCT t1.name, t1.employee_name from
            tabEmployee t1 where t1.status != "left" and (t1.name LIKE '%{text}%' or t1.employee_name LIKE '%{text}%') 
            ORDER  BY t1. employee_name limit {skip}, {limit} """.format(text=text, skip=start, limit=page_len))


@frappe.whitelist()
def get_directors(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""
		SELECT u.name, concat(u.first_name, ' ', u.last_name)
		FROM tabUser u, `tabHas Role` r
		WHERE u.name = r.parent AND r.role = 'Directors' 
		AND u.enabled = 1 AND u.name LIKE %s
	""", ("%" + txt + "%"))


@frappe.whitelist()
def get_approver_authorizer(emp):
    # check if the user reports to any one
    reports_to = frappe.db.sql(""" SELECT reports_to from `tabEmployee` WHERE name="{0}" """.format(emp), as_dict=1)[0]
    if reports_to.reports_to is None:
        data = [dict(approver=emp, authorizer=emp)]
    else:
        data = frappe.db.sql(""" SELECT IFNULL(c.reports_to, '{0}') approver, IFNULL(p.reports_to, c.reports_to) authorizer from
              tabEmployee c JOIN tabEmployee p  ON (c.reports_to = p.name) WHERE c.name="{0}" """.format(emp),
                             as_dict=1)

    # first who the employee reports to
    # and up the ladder
    authorizer = approver = {}
    for datum in data:
        approver = frappe.get_value("Employee", datum.get('approver'), ["name", "user_id", "employee_name"])
        authorizer = frappe.get_value("Employee", datum.get('authorizer'), ["name", "user_id", "employee_name"])

    if not authorizer:
        authorizer = ["", "", ""]
    if not approver:
        approver = ["", "", ""]

    return [{
        "approver": approver[0],
        "authorizer": authorizer[0],
        "approver_name": approver[2],
        "authorizer_name": authorizer[2],
        "approver_user_id": approver[1],
        "authorizer_user_id": authorizer[1]
    }]


@frappe.whitelist()
def resolve_work_order(docname):
    # update without checking permissions
    """ Called from client side on Stop/Unstop event"""
    status = 'Resolved'
    if not frappe.has_permission("Work Order", "write"):
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    frappe.db.sql("update `tabWork Order` set status = 'Resolved', modified='%s',modified_by='%s' , skip_transfer=1"
                  " where name = '%s'" % (datetime.datetime.now(), frappe.session.user,docname))
    frappe.msgprint(_("Work Order has been {0}").format(status))
    return True



@frappe.whitelist()
def get_discount(customer, transation_date):
	d = getdate(transation_date)

	ds_status = frappe.db.sql("SELECT entitled_discount_ FROM `tabCustomer` WHERE"
								   " name= '{1}' AND DATE('{0}') >= discount_start  AND DATE('{0}') <= discount_end".format(d,customer))
	if ds_status:
		return ds_status[0][0]
	else:
		return 0

@frappe.whitelist()
def make_authority_to_load(source_name, target_doc=None):
		def set_missing_values(source, target):
			target.sales_order = source.name

		def update_item(source_doc, target_doc, source_parent):
			pass

		doc = get_mapped_doc("Sales Order", source_name, {
			"Sales Order": {
				"doctype": "Authority to Load",
				"validation": {
					"docstatus": ["=", 1]
				},
				"field_map": {
					"sales_order":"name"
				},
				"add_if_empty": False,
				"postprocess": update_item,
				"condition": lambda doc: doc.docstatus == 1
			},
		}, target_doc, set_missing_values)

		return doc
