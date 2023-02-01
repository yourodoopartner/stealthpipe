# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
{
    'name': 'Sky Custom Stock',
    'version': '15.0.0.1',
    'category': 'Stock',
    'license': 'AGPL-3',
    'description': """
    This module is used to Custom Stock
    """,
    'author': 'Skyscend Business Solutions Pvt. Ltd.',
    'website': 'http://www.skyscendbs.com',
    'depends': ['stock_landed_costs', 'sale'],
    'data': [
        'data/stock_sequence.xml',
        'security/ir.model.access.csv',
        "security/stock_security.xml",
        'wizard/add_landed_cost_wiz_view.xml',
        "views/res_users_view.xml",
        # "views/stock_location.xml"
        'reports/stock_picking_report.xml',
        'reports/bill_of_lading.xml',
        'views/stock_picking.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}
