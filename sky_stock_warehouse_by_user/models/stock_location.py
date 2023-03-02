# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import models, fields


class Location(models.Model):
    _inherit = 'stock.location'

    warehouse_id = fields.Many2one('stock.warehouse', compute='_compute_warehouse_id', store=True)
    is_reserved_location = fields.Boolean('Is Reserved Location')
