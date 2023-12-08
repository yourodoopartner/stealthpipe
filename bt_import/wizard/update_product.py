from odoo import api, fields, models, _
import odoo
from odoo.tools import pycompat
import datetime

import logging
_logger = logging.getLogger(__name__)


class wizard_product_data(models.TransientModel):
    _name = 'wizard.product.data'
    _inherit = 'data_import.wizard'
   
    
    csv_file_name = fields.Char('CSV File Name', size=64)
    csv_file = fields.Binary('Product CSV File', required=True)
    
    
    def upload_product_data(self):
        if self.csv_file:
            list_raw_data = self.get_data_from_attchment(self.csv_file, self.csv_file_name)
            
            if not list_raw_data:
                raise UserError(_("Cannot import blank sheet."))
            count = 0
            for raw in list_raw_data:
                if raw.get('Description',False):
                    print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrawrawraw',raw.get('Description',False))
                    product = raw.get('Description',False)
                    product_id = self.env['product.template'].search([('name','=',product)], limit=1)
                    product_id.standard_price = raw.get('Cost',False) or 0
                    count += 1
                    _logger.info("******************Count................%s", count)
            return True    
    
       
    
    
    
                   
