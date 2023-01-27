# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
{
    'name': 'Purchase Order Total Quantity',
    'version': '15.0.0.1',
    'category': 'Others',
    'license': 'AGPL-3',
    'description': """
    This module is used to set Purchase Order Total Quantity
    """,
    'author': 'Skyscend Business Solutions Pvt. Ltd.',
    'website': 'http://www.skyscendbs.com',
    'depends': ['purchase'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}
