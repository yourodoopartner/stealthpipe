# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import fields, models, api

class ProductProduct(models.Model):
    _inherit = "product.product"

    def update_sales_description(self):
        for product in self:
            product.description_sale = ''
            if product.diameter != 0.0:
                product.description_sale += 'Diameter: ' + str(product.diameter) + ', '

            if product.wall_thickness != 0.0:
                product.description_sale += 'Wall Thickness: ' + str(product.wall_thickness) + ', '

            if product.length != 0.0:
                product.description_sale += 'Length: ' + str(product.length)

    @api.model_create_multi
    def create(self, vals):
        res = super(ProductProduct, self).create(vals)
        for product in res:
            product.update_sales_description()
        return res

    def write(self, vals):
        res = super(ProductProduct, self).write(vals)
        if 'name' in vals or 'diameter' in vals or 'wall_thickness' in vals or 'length' in vals:
            self.update_sales_description()
        return res
