# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BT Stealthpipe Customization',
    'version': '1.0.1',
    'summary': 'BT Stealthpipe Customization',
    'description': """
        BT Stealthpipe Customization.
    """,
    'author': 'BroadTech IT Solutions Pvt Ltd',
    'website': 'http://www.broadtech-innovations.com',
    'depends': ['stock','base','sale','account','sale_management','sky_stock'],
    'data': [
        'security/stock_picking_type_group_view.xml',
        'security/ir.model.access.csv',
        'views/stock_view.xml',
        'wizard/stock_move_report_xls.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
