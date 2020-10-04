from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Human Resources"),
            "items": [
                {
                    "type": "doctype",
                    "name": "Staff Requisition"
                },
                {
                    "type": "doctype",
                    "name": "Staff Replacement"
                },
                {
                    "type": "doctype",
                    "name": "Overtime Request"
                },
                {
                    "type": "doctype",
                    "name": "Overtime Sheet"
                }
            ]
        },
        {
            "label": _("Buying"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Purchase Requisition",
                    "description": _("Purchase Requisition"),
                },
            ]
        },
        {
            "label": _("Selling"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Authority to Load",
                    "description": _("Authority to Load"),
                },
                {
                    "type": "doctype",
                    "name": "Call Log",
                    "description": _("Call Log"),
                },
            ]
        },
        {
            "label": _("Support"),
            "icon": "icon-star",
            "items": [
                {
                    "type": "doctype",
                    "name": "Work Card",
                    "description": _("Work Card"),
                },
                {
                    "type": "doctype",
                    "name": "Helpdesk Ticket",
                    "description": _("Helpdesk Ticket"),
                },
            ]
        },
    ]
