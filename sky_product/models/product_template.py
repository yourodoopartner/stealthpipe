from odoo import fields, models, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    diameter = fields.Float(string='Diameter')
    wall_thickness = fields.Float(string='Wall Thickness')
    length = fields.Float(string='Length')


class ProductProduct(models.Model):
    _inherit = "product.product"
    
    def update_sales_description(self):
        self.description_sale = ''
        if self.diameter != 0.0:
            self.description_sale += 'Diameter: ' + str(self.diameter) + ', '

        if self.wall_thickness != 0.0:
            self.description_sale += 'Wall Thickness: ' + str(self.wall_thickness) + ', '

        if self.length != 0.0:
            self.description_sale += 'Length: ' + str(self.length)

    @api.model_create_multi
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        res.update_sales_description()
        return res

    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if 'name' in vals or 'diameter' in vals or 'wall_thickness' in vals or 'length' in vals:
            self.update_sales_description()
        return res
