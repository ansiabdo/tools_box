from frappe import _

def get_data():
	return {
		'fieldname': 'reference_docname',
		'transactions': [
			{
				'label': _('Transactions'),
				'items': ['Purchase Order']
			},
		]
	}