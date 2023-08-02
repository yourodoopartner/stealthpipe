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
    'name': 'Sky Custom Invoice',
    'version': '15.0.0.1',
    'category': 'Others',
    'license': 'AGPL-3',
    'description': """
    This module is used for Customs Invoice report
    """,
    'author': 'Skyscend Business Solutions',
    'website': 'http://www.skyscendbs.com',
    'depends': ['purchase', 'sale'],
    'data': [
        'views/template_view.xml',
        'views/purchase_canada_custom_report_view.xml',
        'views/sale_canada_custom_report_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
