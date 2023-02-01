# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    landed_cost = fields.Float('Landed Cost')
    total_landed_cost = fields.Float('Total Cost ', compute='_cal_total_landed_cost')

    @api.depends('landed_cost', 'price_unit')
    def _cal_total_landed_cost(self):
        """
        This method is used to get the sum of the product unit price and its landed cost.
        ------------------------------------------------------------------------------------
        @param self: object pointer
        :return:
        """
        for rec in self:
            rec.total_landed_cost = rec.landed_cost + rec.price_unit
