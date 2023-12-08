# -*- coding: utf-8 -*-
##############################################################################

import csv
import base64
import os
import xlrd
from io import StringIO
from io import BytesIO

from odoo import api, fields, models, _
from odoo.tools.translate import _
from odoo import tools as openerp_tools
from odoo.exceptions import UserError, RedirectWarning, ValidationError

class data_import_wizard(models.TransientModel):
    _name = 'data_import.wizard'
    _description = 'Import Data'
    
    def get_data_from_attchment(self, binary_file, file_name):
        list_raw = []
        if '.csv' in file_name:
            response =(base64.b64decode(binary_file))
            res = str(response,'utf-8')
           
            for raw_data in csv.DictReader(StringIO(res),delimiter=',', quotechar='"'):
                list_raw.append(raw_data)
        if '.xls' in file_name or '.xlsx' in file_name:   
            path = openerp_tools.config['addons_path'].split(",")[-1]
            if '.xls' in file_name:
                fullpath = os.path.join(path, 'emp_attendance.xls')
            if '.xlsx' in file_name:
                fullpath = os.path.join(path, 'emp_attendance.xlsx')
            with open(fullpath, 'wb') as f:
                f.write(base64.decodebytes(binary_file))
            rb = xlrd.open_workbook(fullpath)
            sheet = rb.sheet_by_index(0)
            headers = []
            for rownum in range(sheet.nrows):
              row = sheet.row_values(rownum)
              if headers:
                  raw_data = {}
                  cell_count = -1
                  for cell in row:
                      cell_count = cell_count + 1
                      raw_data.update({headers[cell_count] : cell})
                  list_raw.append(raw_data)    
              if not headers:
                  headers = row
        return list_raw
                
