# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
{
    'name': 'Invoice and Vendor Bills Total Quantity',
    'version': '15.0.0.1',
    'category': 'Others',
    'license': 'AGPL-3',
    'description': """
    This module is used to set Invoice and Vendor Bills Total Quantity
    """,
    'author': 'Skyscend Business Solutions Pvt. Ltd.',
    'website': 'http://www.skyscendbs.com',
    'depends': ['account'],
    'data': [
        'views/account_move_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}
