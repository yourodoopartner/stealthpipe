from odoo import models, fields


class AddLandedAm(models.Model):
    _name = "landed.cost.amt"
    _description = "Land Cost AMT"

    landed_cost = fields.Many2one('product.product', 'Product')
    amount = fields.Float('Amount')
    cost_id = fields.Many2one('stock.picking', 'Cost')
    split_method = fields.Selection(selection=[
        ('equal', 'Equal'),
        ('by_quantity', 'By Quantity'),
        ('by_current_cost_price', 'By Current Cost'),
        ('by_weight', 'By Weight'),
        ('by_volume', 'By Volume'),
    ], string='Split Method', required=True)
    account_id = fields.Many2one('account.account', 'Account', domain=[('deprecated', '=', False)])
