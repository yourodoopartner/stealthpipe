# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import fields, models, api
import csv
from odoo.modules.module import get_module_path


class ProductTemplate(models.Model):
    _inherit = "product.template"

    diameter = fields.Float(string='Diameter')
    wall_thickness = fields.Float(string='Wall Thickness', digits=(16, 3))
    length = fields.Float(string='Length')

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
        res = super(ProductTemplate, self).create(vals)
        for product in res:
            product.update_sales_description()
        return res

    def write(self, vals):
        res = super(ProductTemplate, self).write(vals)
        if 'name' in vals or 'diameter' in vals or 'wall_thickness' in vals or 'length' in vals:
            self.update_sales_description()
        return res

    def import_product_weight(self):
        product_data_dict = {}
        for product in self.search([]):
            product_data_dict.update({product.name:product.id})
        file_path = get_module_path('sky_product')
        with open(file_path+'/static/Product Template.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            for row in csvreader:
                if row[1] in product_data_dict:
                    query = """
                                UPDATE product_product SET weight = %s WHERE product_tmpl_id = %s
                            """
                    self._cr.execute(query, (tuple([row[5]]), tuple([product_data_dict.get(row[1])])))

    def import_product_template(self):
        product_name_list = ['Grade:A500 & Range: R1 – 16’ / 24’', 'Grade:A500 & Range: R2 – 25’ / 34’',
                             'Grade:A500 & Range: R3 – 35’ / 48’', 'Grade:A500 & Range: R4 – 49’ / 62’',
                             'Grade:A500 & Range: HR', 'Grade:A500 & Range: Shorts – 2’ / 15’',

                             'Grade:A-252 & Range: R1 – 16’ / 24’', 'Grade:A-252 & Range: R2 – 25’ / 34’',
                             'Grade:A-252 & Range: R3 – 35’ / 48’', 'Grade:A-252 & Range: R4 – 49’ / 62’',
                             'Grade:A-252 & Range: HR', 'Grade:A-252 & Range: Shorts – 2’ / 15’',

                             'Grade:A-53 & Range: R1 – 16’ / 24’', 'Grade:A-53 & Range: R2 – 25’ / 34’',
                             'Grade:A-53 & Range: R3 – 35’ / 48’', 'Grade:A-53 & Range: R4 – 49’ / 62’',
                             'Grade:A-53 & Range: HR', 'Grade:A-53 & Range: Shorts – 2’ / 15’']
        count = 0
        file_path = get_module_path('sky_product')
        with open(file_path+'/static/Product Template.csv', 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            header = next(csvreader)
            for row in csvreader:
                for new_name in product_name_list:
                    product_dict = {
                        'name': row[1] +' '+ new_name,
                        'uom_id': 18,
                        'uom_po_id': 18,
                        'default_code': row[2],
                        'detailed_type': 'product',
                        'invoice_policy': 'delivery',
                        'purchase_method': 'receive',
                        'diameter': row[3],
                        'wall_thickness': row[4],
                        'weight': row[5],
                    }
                    self.create(product_dict)
                    count += 1

