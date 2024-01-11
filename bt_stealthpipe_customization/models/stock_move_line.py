from odoo import models, fields, api, _


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    diameter = fields.Float('Diameter', related='product_id.diameter', store=True)



class StockValuationLayer(models.Model):
    _inherit = 'stock.valuation.layer'

    diameter = fields.Float('Diameter', related='product_id.diameter', store=True)


