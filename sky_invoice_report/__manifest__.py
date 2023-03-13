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
    'name': 'Sky Invoice Report',
    'version': '15.0.0.1',
    'category': 'Others',
    'license': 'AGPL-3',
    'description': """
    This module is used for customized Invoice report
    """,
    'author': 'Skyscend Business Solutions',
    'website': 'http://www.skyscendbs.com',
    'depends': ['account',],
    'data': [
        'views/invoce_paper_format.xml',
        'views/invoice_report_view.xml',
    ],
    'installable': True,
    'auto_install': False
}
