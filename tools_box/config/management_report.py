from __future__ import unicode_literals
from frappe import _


def get_data():
    return [
        {
            "label": _("Finance"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Profit and Loss Statement",
                    "label": "Profit and Loss Statement"
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Accounts Receivable",
                    "label": "Accounts Receivable"
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Accounts Payable",
                    "label": "Accounts Payable"
                },
            ]
        }, {
            "label": _("Selling"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Sales By Customer",
                    "label": "Sales By Customer (Top 50)"
                },
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Sales By Product",
                }, {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Sales Representative Scorecard",
                }
            ]
        },{
            "label": _("Stock"),
            "items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Raw Material Valuation",
                    "doctype": "Stock Ledger Entry"
                }, {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Finished Goods Valuation",
                    "doctype": "Stock Ledger Entry"
                }, {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Stock Balance Summary",
                    "doctype": "Stock Ledger Entry"
                }
          ]
        },
    ]
