# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cint, flt, cstr, comma_or

""" 
    This is suppose to return some kind of information used as addon
    the Goal is to maintain all icons that's not ERPNext's from a centralized location
    thus making it easy to amend or extend
"""


def get_selling_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Authority to Load"),
        "name": "Authority to Load",
        "icon": "icon-sitemap",
        "link": "List/Authority to Load",
        "description": _("Authority to Load"),
    }])

def get_account_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Asset Transfer Form"),
        "name": "Asset Transfer Form",
        "icon": "icon-sitemap",
        "link": "List/Asset Transfer Form",
        "description": _("Asset Transfer Form"),
    }], label="Additional")

def get_stock_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Quality Control Material Acceptance Form"),
        "name": "Quality Control Material Acceptance Form",
        "icon": "icon-sitemap",
        "link": "List/Quality Control Material Acceptance Form",
        "description": _("Quality Control Material Acceptance Form"),
    }])

def get_production_section():
    return __default_item([
    ], label="Additional")

def get_waste_section():
    return __default_item([

    ], label="Production Waste")

def get_maintenance_section():
    return __default_item([
        {
            "type": "doctype",
            "label": _("Equipment Support"),
            "name": "Equipment Support",
            "icon": "icon-sitemap",
            "link": "List/Equipment Support",
            "description": _("Equipment Support"),
        },
        {
            "type": "doctype",
            "label": _("Job Card"),
            "name": "Job Card",
            "icon": "icon-sitemap",
            "link": "List/Job Card",
            "description": _("Job Card"),
        },
        {
            "type": "doctype",
            "label": _("Equipment Maintenance Log"),
            "name": "Equipment Maintenance Log",
            "icon": "icon-sitemap",
            "link": "List/Equipment Maintenance Log",
            "description": _("Equipment Maintenance Log"),
        },
        {
            "type": "doctype",
            "label": _("Computing Asset Inspection Checklist"),
            "name": "Computing Asset Inspection Checklist",
            "icon": "icon-sitemap",
            "link": "List/Computing Asset Inspection Checklist",
            "description": _("Computing Asset Inspection Checklist"),
        },
        {
            "type": "doctype",
            "label": _("Fixed Asset Inspection Checklist"),
            "name": "Fixed Asset Inspection Checklist",
            "icon": "icon-sitemap",
            "link": "List/Fixed Asset Inspection Checklist",
            "description": _("Fixed Asset Inspection Checklist"),
        },
        {
            "type": "doctype",
            "label": _("Generator Fuel Consumption Log"),
            "name": "Generator Fuel Consumption Log",
            "icon": "icon-sitemap",
            "link": "List/Generator Fuel Consumption Log",
            "description": _("Generator Fuel Consumption Log"),
        },
        {
            "type": "doctype",
            "label": _("Daily Generator Activity Log"),
            "name": "Daily Generator Activity Log",
            "icon": "icon-sitemap",
            "link": "List/Daily Generator Activity Log",
            "description": _("Daily Generator Activity Log"),
        }
    ], label = "Extras")

def get_purchasing_section():
    return __default_item([
        {
            "type": "doctype",
            "label": _("Purchase Requisition"),
            "name": "Purchase Requisition",
            "icon": "icon-sitemap",
            "link": "List/Purchase Requisition",
            "description": _("Purchase Requisition"),
        }
    ], label = "Additionals")

def get_hr_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Requisition"),
        "name": "Requisition",
        "icon": "icon-sitemap",
        "link": "List/Requisition",
        "description": _("Requisition"),
    },{
        "type": "doctype",
        "label": _("Staff Requisition Form"),
        "name": "Staff Requisition Form",
        "icon": "icon-sitemap",
        "link": "List/Staff Requisition Form",
        "description": _("Staff Requisition Form"),
    }, {
        "type": "doctype",
        "label": _("Staff Replacement Request Form"),
        "name": "Staff Replacement Request Form",
        "icon": "icon-sitemap",
        "link": "List/Staff Replacement Request Form",
        "description": _("Staff Replacement Request Form"),
    }, {
        "type": "doctype",
        "label": _("Overtime Request"),
        "name": "Overtime Request",
        "icon": "icon-sitemap",
        "link": "List/Overtime Request",
        "description": _("Overtime Request"),
    }, {
        "type": "doctype",
        "label": _("Overtime Sheet"),
        "name": "Overtime Sheet",
        "icon": "icon-sitemap",
        "link": "List/Overtime Sheet",
        "description": _("Overtime Sheet"),
    }, {
        "type": "doctype",
        "label": _("Stationaries Request"),
        "name": "Stationaries Request",
        "icon": "icon-sitemap",
        "link": "List/Stationaries Request",
        "description": _("Stationaries Request"),
    },{
        "type": "doctype",
        "label": _("Stationaries Log"),
        "name": "Stationaries Log",
        "icon": "icon-sitemap",
        "link": "List/Stationaries Log",
        "description": _("Stationaries Log"),
    },
    ])

def get_support_section():
    return __default_item([{
        "type": "doctype",
        "label": _("Helpdesk Ticket"),
        "name": "Helpdesk Ticket",
        "icon": "icon-sitemap",
        "link": "List/Helpdesk Ticket",
        "description": _("Helpdesk Ticket"),
    }, {
        "type": "doctype",
        "label": _("Job Card"),
        "name": "Job Card",
        "icon": "icon-sitemap",
        "link": "List/Job Card",
        "description": _("Job Card"),
    }])

def get_extra_hr_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "Expense Claim Report",
            "doctype": "Expense Claim",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Employee Advance Report",
            "doctype": "Employee Advance",
            "is_query_report": True,
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Employee Leave Balance",
            "doctype": "Leave Application"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Employee Birthday",
            "doctype": "Employee"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Employees working on a holiday",
            "doctype": "Employee"
        },
        {
            "type": "report",
            "name": "Employee Status Summary",
            "doctype": "Employee",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Employee Report Summary",
            "doctype": "Employee",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Employee Pay Summary",
            "doctype": "Employee",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Employee Information",
            "doctype": "Employee"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Monthly Salary Register",
            "doctype": "Salary Slip"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Monthly Attendance Sheet",
            "doctype": "Attendance"
        }, ])

def get_extra_waste_reports():
    return __default_rep_items([

    ], label="Production Waste Reports")

def get_extra_production_reports():
    return __default_rep_items([

    ])

def get_extra_maintenance_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "Daily Generator Activity Log Report",
            "doctype": "Daily Generator Activity Log",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Generator Fuel Consumption Log Report",
            "doctype": "Generator Fuel Consumption Log",
            "is_query_report": False,
        },
        {
            "type": "report",
            "name": "Fixed Asset Inspection Checklist Report",
            "doctype": "Fixed Asset Inspection Checklist",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Computing Asset Inspection Checklist Report",
            "doctype": "Computing Asset Inspection Checklist",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Equipment Maintenance Log Report",
            "doctype": "Equipment Maintenance Log Report",
            "is_query_report": True,
        },
        {
            "type": "report",
            "name": "Work Order Completion Report",
            "doctype": "Work Order Completion Report",
            "is_query_report": True,
        }
    ])

def get_extra_account_reports():
    return __default_rep_items([])

def get_extra_selling_reports():
    return __default_rep_items([
        {
            "type": "report",
            "is_query_report": True,
            "name": "Sales By Customer",
            "label": "Sales By Customer (Top 50)"
        },
        {
            "type": "report",
            "is_query_report": True,
            "name": "Sales By Product"
        },{
            "type": "report",
            "is_query_report": True,
            "name": "Sales Representative Scorecard"
        }])

def get_extra_purchase_reports():
    return __default_rep_items([
    ])

def get_extra_stock_reports():
    return __default_rep_items([
        {
            "type": "report",
            "is_query_report": True,
            "name": "Raw Material Valuation",
            "doctype": "Stock Ledger Entry"
        },{
            "type": "report",
            "is_query_report": True,
            "name": "Finished Goods Valuation",
            "doctype": "Stock Ledger Entry"
        },{
            "type": "report",
            "is_query_report": True,
            "name": "Stock Balance Summary",
            "doctype": "Stock Ledger Entry"
        }
    ])

def get_extra_support_reports():
    return __default_rep_items([
        {
            "type": "report",
            "name": "HelpDesk Report",
            "doctype": "Helpdesk Ticket",
            "is_query_report": True
        },
        {
            "type": "report",
            "name": "Job Card Status Report",
            "doctype": "Job Card",
            "is_query_report": True
        },
        {
            "type": "report",
            "name": "Job Card Cost Report",
            "doctype": "Job Card",
            "is_query_report": True
        },
        {
            "type": "report",
            "name": "Job Card Completion Report",
            "doctype": "Job Card",
            "is_query_report": True
        },
    ])

def __default_item(items, label="Extras"):
    return {
        "label": label,
        "items": items,
        "icon": "icon-cog"
    }

def __default_rep_items(items, label="Extra Reports"):
    return {
        "label": label,
        "items": items
    }
