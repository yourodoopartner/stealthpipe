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

    landed_cost = fields.Float('Landed Cost', copy=False, group_operator="avg")
    landed_cost_per_foot = fields.Float('Landed Cost per foot', copy=False)
    total_landed_cost = fields.Float('Total Cost ', compute='_cal_total_landed_cost', copy=False)
    product_cost = fields.Float('Product Cost', compute='_cal_product_cost', copy=False)
    final_cost = fields.Float('Final Cost', compute='_cal_final_cost', copy=False)
    lengths = fields.Float('Lengths', related='sale_line_id.lengths', store=True, readonly=False)
    diameter = fields.Float('Diameter', store=True, readonly=False)

    @api.depends('landed_cost', 'product_cost')
    def _cal_total_landed_cost(self):
        """
        This method is used to get the sum of the product unit price and its landed cost.
        ------------------------------------------------------------------------------------
        @param self: object pointer
        :return:
        """
        for rec in self:
            rec.total_landed_cost = rec.landed_cost + rec.product_cost

    @api.depends('price_unit', 'product_uom_qty')
    def _cal_product_cost(self):
        """
        This method is used to calculate the product cost.[Depends on product cost and its quantity.]
        ----------------------------------------------------------------------------------------------
        @:param self: object pointer
        :return:
        """
        for rec in self:
            rec.product_cost = rec._get_price_unit() * rec.product_uom_qty

    @api.depends('total_landed_cost', 'product_uom_qty')
    def _cal_final_cost(self):
        """
        This method is used to calculate the final cost.[Depends on total cost and product quantity]
        ----------------------------------------------------------------------------------------------
        @:param self: object pointer
        :return:
        """
        for rec in self:
            if rec.product_uom_qty > 0:
                rec.final_cost = rec.total_landed_cost / rec.product_uom_qty
            else:
                rec.final_cost = 0.0
