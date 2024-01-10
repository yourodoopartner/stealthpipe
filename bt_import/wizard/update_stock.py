from odoo import api, fields, models, _
from odoo.tools import pycompat
import odoo

import logging
_logger = logging.getLogger(__name__)

class WizardUpdateStock(models.TransientModel):
    _name = 'wizard.update.stock'
    _inherit = 'data_import.wizard'
    
    csv_file_name = fields.Char('CSV File Name', size=64)
    csv_file = fields.Binary('CSV File', required=True)
    
    
    def create_move(self, product, qty, price, location, dest_location):
        move_vals = {
            'name': _('Product Inventory Update'),
            'product_id': product.id,
            'product_uom': product.uom_id and product.uom_id.id or False,
            'product_uom_qty': qty,
            'price_unit': price,
            'company_id': self.env.user.company_id.id,
            'state': 'confirmed',
            'location_id': location.id,
            'location_dest_id': dest_location.id,
            'move_line_ids': [(0, 0, {
                'product_id': product.id,
                'product_uom_id': product.uom_id and product.uom_id.id or False,
                'qty_done': qty,
                'location_id': location.id,
                'location_dest_id': dest_location.id,
                'company_id': self.env.user.company_id.id,
                'lot_id': False,
                'package_id': False,
                'result_package_id': False,
                'owner_id': False,
            })]
        }
        move = self.env['stock.move'].create(move_vals)
        move._action_done()
        return True
    
    def upload_product_stock(self):
        if self.csv_file:
            list_raw_data = self.get_data_from_attchment(self.csv_file, self.csv_file_name)
            
            if not list_raw_data:
                raise UserError(_("Cannot import blank sheet."))
            count = 0
            not_product_list = []
            print('lllllllllllllllllllllll***********')
            for raw in list_raw_data:
                if raw.get('Description',False):
                    print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrawrawraw',raw.get('Description',False))
                    product = raw.get('Description',False)
                    product_id = self.env['product.template'].search([('name','=',product)], limit=1)
                    if not product_id:
                        not_product_list.append(product)   
                    if product_id:
                        # product_id.standard_price = raw.get('Cost',False) or 0
                        price = raw.get('Cost',False) or 0
                        product_domain = [('name','=',product), ('product_tmpl_id', '=', product_id.id)]
                        product_variant_id = self.env['product.product'].search(product_domain, limit=1)
                        print('pppppppppppppppppp',product_variant_id)
                        
                        if product_variant_id:
                            stock_location = self.env['stock.location'].search([('name','=','Stock'),('location_id.name','=', raw.get('Warehouse',False))])
                            virtual_location = product_variant_id.property_stock_inventory   
                            if stock_location and virtual_location:
                                qty = float(raw.get('Total Footage',0))
                                if qty > 0:
                                    move = self.create_move(product_variant_id, qty, price, virtual_location, stock_location)
                                if qty < 0:
                                    move = self.create_move(product_variant_id, -qty, price, stock_location, virtual_location)
                                count += 1
            _logger.info("******************Count................%s", count)
            _logger.info("******************not product_variant_id.............%s", not_product_list)



