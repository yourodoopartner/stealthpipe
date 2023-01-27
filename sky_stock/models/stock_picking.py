# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import models, fields, api, _
from datetime import date


class Picking(models.Model):
    _inherit = "stock.picking"

    bill_of_lading = fields.Char('Bill Of Lading')
    landed_cost_ids = fields.One2many('landed.cost.amt', 'cost_id', string='Landed Cost')

    @api.model_create_multi
    def create(self, vals_lst):
        """
        Overridden create() method to set the bill_of_lading on the Stock Picking
        -------------------------------------------------------------------------
        :param vals_lst: A list of dictionary containing fields and values
        :return: A newly created recordset.
        """
        res = super(Picking, self).create(vals_lst)
        for picking in res:
            if picking.picking_type_code == "incoming":
                picking.bill_of_lading = self.env['ir.sequence'].next_by_code('bill.lading.seq', sequence_date=False) or _('New')
        return res

    def button_validate(self):
        """
        Overridden button_validate() method and create Stock Landed Cost.
        ------------------------------------------------------------------
        :param vals_lst: A list of dictionary containing fields and values
        :return: A newly created recordset.
        """
        result = super(Picking, self).button_validate()
        stock_landed_cost_obj = self.env['stock.landed.cost']
        oder_line_rec = []
        for picking in self:
            if picking.picking_type_code == 'incoming':
                for line in picking.landed_cost_ids:
                    oder_line_rec.append(
                        (0, 0, {
                            'product_id': line.landed_cost.id,
                            'name': line.landed_cost.name,
                            'split_method': line.split_method,
                            'account_id': line.account_id.id,
                            'price_unit': line.amount
                        })
                    )
                land_cost_id = stock_landed_cost_obj.create({
                    'date': date.today(),
                    'picking_ids': [(4, picking.id)],
                    'cost_lines': oder_line_rec
                })
                land_cost_id.compute_landed_cost()
                land_cost_id.button_validate()
        return result
