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
    'depends': ['stock_landed_costs', 'sale', 'sky_stock_warehouse_by_user', 'delivery'],
    'data': [
        'data/stock_sequence.xml',
        'security/ir.model.access.csv',
        'wizard/add_landed_cost_wiz_view.xml',
        'wizard/add_operation_type_wiz_view.xml',
        'reports/stock_picking_report.xml',
        'reports/bill_of_lading.xml',
        'views/stock_picking.xml',
        'views/sale_order_line_view.xml',
        'views/purchase_order_line_view.xml',
        'views/stock_quant.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}
