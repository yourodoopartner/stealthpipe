
from odoo import models, fields, api, _


class StockMove(models.Model):
    _inherit = 'stock.move'

    pieces = fields.Float('Pieces')



