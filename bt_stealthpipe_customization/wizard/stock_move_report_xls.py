# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api, _
import xlwt
import io
import base64
from xlwt import easyxf
from PIL import Image
import tempfile, os
from io import BytesIO

import datetime
from datetime import time, timedelta


class PrintStockMove(models.TransientModel):
    _name = "print.stock.move"
    

    file = fields.Binary('Stock Move Report')
    file_name = fields.Char('File Name')
    report_printed = fields.Boolean('Report Printed')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', default=fields.Date.context_today)
    
    
    def action_print(self):
        workbook = xlwt.Workbook()
        column_heading_style = easyxf('font:height 200;font:bold True;align:horiz left;align:vertical center;')
        worksheet = workbook.add_sheet('Stock Move xls')
        row = 0
        # active_list = self._context.get('active_ids', [])
        for wizard in self:
                stock_moves = []
                if wizard.start_date:
                    stock_moves = self.env['stock.move'].search([('date', '>=', wizard.start_date), ('date', '<=', wizard.end_date)])
                else:
                    stock_moves = self.env['stock.move'].search([('date', '<=', wizard.end_date)])
                
                # Description (Product), Diameter, Quantity in Feet (Total Footage), Quantity in Lengths (Pieces), Landed Cost (Cost).
                worksheet.write(row, 0, _('Description'), column_heading_style)
                worksheet.write(row, 1, _('Diameter'), column_heading_style)
                worksheet.write(row, 2, _('Quantity in Feet'), column_heading_style)
                worksheet.write(row, 3, _('Quantity in Lengths'), column_heading_style)
                worksheet.write(row, 4, _('Landed Cost'), column_heading_style)
                worksheet.col(0).width = 10000
                worksheet.col(1).width = 2500
                worksheet.col(2).width = 4500
                worksheet.col(3).width = 4600
                worksheet.col(4).width = 3500
                
                row = 1
                for line in stock_moves:
                    worksheet.write_merge(row, row, 0, 0, line.product_id.name, easyxf('align:vertical center;'))
                    worksheet.write_merge(row, row, 1, 1, line.product_id.diameter or '', easyxf('align:vertical center;'))
                    worksheet.write_merge(row, row, 2, 2, line.product_uom_qty or 0, easyxf('align:vertical center;'))
                    worksheet.write_merge(row, row, 3, 3, line.pieces or line.lengths or 0, easyxf('align:vertical center;'))
                    worksheet.write_merge(row, row, 4, 4, line.price_unit or 0, easyxf('align:vertical center;'))
                    row += 1
         
                fp = io.BytesIO()
                workbook.save(fp)
                excel_file = base64.encodestring(fp.getvalue())
                wizard.file = excel_file
                wizard.file_name = 'Stock Move.xls'
                wizard.report_printed = True
                fp.close()
                return {
                    'view_mode': 'form',
                    'res_id': wizard.id,
                    'res_model': 'print.stock.move',
                    'view_type': 'form',
                    'type': 'ir.actions.act_window',
                    'context': self.env.context,
                    'target': 'new',
                }

    
    
    
    
