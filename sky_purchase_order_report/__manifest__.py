{
    'name': 'Purchase Order Report',
    'version': '15.0.0.1',
    'category': 'Others',
    'license': 'AGPL-3',
    'description': """
    This module is used to customize purchase report
    """,
    'author': 'Skyscend Business Solutions Pvt. Ltd.',
    'website': 'http://www.skyscendbs.com',
    'depends': ['purchase'],
    'data': [
        'views/customize_purchase_report_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}