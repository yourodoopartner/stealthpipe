# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import api, fields, models


class Users(models.Model):
    _inherit = 'res.users'

    warehouse_ids = fields.Many2many('stock.warehouse', string="Warehouses")
