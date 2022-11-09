from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    diameter = fields.Float(string='Diameter')
    wall_thickness = fields.Float(string='Wall Thickness')
