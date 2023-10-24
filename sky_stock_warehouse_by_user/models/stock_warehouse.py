# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import models, fields, exceptions


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    def write(self, values):
        # Prevent renaming of warehouses by internal users
        if self.env.user.has_group('stock.group_stock_manager') and 'name' in values or 'code' in values:
            raise exceptions.UserError("Internal users cannot rename Warehouses and Short Name.")
        return super(StockWarehouse, self).write(values)