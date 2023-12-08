# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'BT Stealthpipe Import',
    'summary': 'BT Import',
    'description': """
        XLSX Import of inventory
    """,
    'version': '15.1.0',
    'depends': ['stock',
                ],
    'data' : [
        'security/ir.model.access.csv',
        'wizard/update_stock.xml',
        'wizard/update_product.xml',
        'views/product_view.xml'
     ],
    
    'test': [
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,

}
