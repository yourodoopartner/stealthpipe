from odoo import models, fields, api, _


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    diameter = fields.Float('Diameter', related='product_id.diameter', store=True)


