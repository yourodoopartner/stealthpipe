from odoo import models, fields


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lengths = fields.Float('Lengths')