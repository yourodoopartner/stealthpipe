# -*- encoding: utf-8 -*-
##############################################################################
#
#    Skyscend Business Solutions
#    Copyright (C) 2019 (http://www.skyscendbs.com)
#    Skyscend Business Solutions Pvt. Ltd.
#    Copyright (C) 2020 (http://wee.skyscendbs.com)
#
##############################################################################
{
    'name': 'Product Import',
    'version': '15.0.0.1',
    'category': 'Others',
    'license': 'AGPL-3',
    'description': """
    This module is used to import Product
    """,
    'author': 'Skyscend Business Solutions',
    'website': 'http://www.skyscendbs.com',
    'depends': ['base', 'stock'],
    'data': [
        'views/product_template.xml',
        'views/product_product.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False
}

