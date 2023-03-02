# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import models, fields, api


class AddLandedWiz(models.TransientModel):
    _name = "landed.cost.wiz"
    _description = 'range sequence wizard'

    landed_cost_ids = fields.One2many('landed.cost.amount', 'cost_id', string='Landed Cost')

    def add_cost(self):
        for line in self.landed_cost_ids:
            for record in self.env['stock.picking'].browse(self._context.get('active_id')):
                record.write({
                    'landed_cost_ids': [
                        (0, 0, {
                            'product_id': line.product_id.id,
                            'split_method': line.split_method,
                            'account_id': line.account_id.id,
                            'amount': line.amount
                        })]
                })


class AddLanded(models.TransientModel):
    _name = "landed.cost.amount"
    _description = "Leaded Cost Amount"

    product_id = fields.Many2one('product.product', 'Product')
    split_method = fields.Selection(selection=[
        ('equal', 'Equal'),
        ('by_quantity', 'By Quantity'),
        ('by_current_cost_price', 'By Current Cost'),
        ('by_weight', 'By Weight'),
        ('by_volume', 'By Volume'),
    ], string='Split Method', required=True)
    account_id = fields.Many2one('account.account', 'Account', domain=[('deprecated', '=', False)])
    amount = fields.Float('Amount')
    cost_id = fields.Many2one('landed.cost.wiz', 'Cost')

    @api.onchange('product_id')
    def onchange_product_id(self):
        self.split_method = self.product_id.product_tmpl_id.split_method_landed_cost or self.split_method or 'equal'
        accounts_data = self.product_id.product_tmpl_id.get_product_accounts()
        self.account_id = accounts_data['stock_input']
