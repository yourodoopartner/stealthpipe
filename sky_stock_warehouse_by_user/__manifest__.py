# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
{
    'name': ' Sky Stock Warehouse By User',
    'version': '15.0.0.1',
    'category': 'Stock',
    'license': 'AGPL-3',
    'description': """
     This module is used to show Delivery orders based on group.
     """,
    'author': 'Skyscend Business Solutions Pvt. Ltd.',
    'website': 'https://www.skyscendbs.com',
    'depends': ['stock'],
    'data': [
        'security/stock_warehouse_security.xml',
        'views/res_users_view.xml',
        'views/stock_location_form_view.xml',

    ],
    'installable': True,
    'auto-install': True
}
