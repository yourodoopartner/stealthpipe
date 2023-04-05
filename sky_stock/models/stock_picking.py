# -*- encoding: utf-8 -*-
##########################################################################################
#
#    Copyright (C) 2019 Skyscend Business Solutions (https://www.skyscendbs.com)
#    Copyright (C) 2020 Skyscend Business Solutions Pvt. Ltd. (https://www.skyscendbs.com)
#
##########################################################################################
from odoo import models, fields, api, _, tools
from datetime import date
from odoo.exceptions import UserError


class Picking(models.Model):
    _inherit = "stock.picking"

    bill_of_lading = fields.Char('Bill Of Lading')
    landed_cost_ids = fields.One2many('landed.cost.amt', 'cost_id', string='Landed Cost')
    x_studio_consignee = fields.Char('Consignee')
    x_studio_freight_terms = fields.Selection([('Prepaid','Prepaid'),('Collect','Collect')], string="Freight Terms")

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
            if picking.picking_type_code in ["incoming", "outgoing"]:
                picking.bill_of_lading = self.env['ir.sequence'].next_by_code('bill.lading.seq',
                                                                              sequence_date=False) or _('New')
        return res

    def _action_done(self):
        """
        Overridden _action_done() method and create Stock Landed Cost.
        ------------------------------------------------------------------
        :param vals_lst: A list of dictionary containing fields and values
        :return: A newly created recordset.
        """
        result = super(Picking, self)._action_done()
        for picking in self.env['stock.picking'].browse(self._context.get('button_validate_picking_ids')):
            oder_line_rec = []
            if picking.picking_type_code == 'incoming' and self._context and self._context.get(
                    'landed_cost') and not self._context.get('cancel_backorder'):
                for line in picking.landed_cost_ids:
                    oder_line_rec.append(
                        (0, 0, {
                            'product_id': line.product_id.id,
                            'name': line.product_id.name,
                            'split_method': line.split_method,
                            'account_id': line.account_id.id,
                            'price_unit': line.amount
                        })
                    )
                land_cost_id = self.env['stock.landed.cost'].create({
                    'date': date.today(),
                    'picking_ids': [(4, picking.id)],
                    'cost_lines': oder_line_rec
                })
                self.compute_landed_cost_amount()
                land_cost_id.button_validate()
        return result

    def compute_landed_cost_amount(self):
        """
        This method is used to calculate the landed cost amount in stock move.
        ----------------------------------------------------------------------
        @param self: object pointer
        :return: boolean : Landed cost value
        """
        towrite_dict = {}
        adjustment_list = []
        for cost in self:
            rounding = cost.company_id.currency_id.rounding
            total_qty = 0.0
            total_cost = 0.0
            total_weight = 0.0
            total_volume = 0.0
            total_line = 0.0
            all_val_line_values = cost.get_valuation_lines()
            for val_line_values in all_val_line_values:
                for cost_line in cost.landed_cost_ids:
                    val_line_values.update({'cost_id': cost.id, 'cost_line_id': cost_line.id})
                    adjustment_dict = val_line_values.copy()
                    adjustment_list.append(adjustment_dict)

                total_qty += val_line_values.get('quantity', 0.0)
                total_weight += val_line_values.get('weight', 0.0)
                total_volume += val_line_values.get('volume', 0.0)

                former_cost = val_line_values.get('former_cost', 0.0)
                # round this because former_cost on the valuation lines is also rounded
                total_cost += cost.company_id.currency_id.round(former_cost)

                total_line += 1
            for line in cost.landed_cost_ids:
                value_split = 0.0
                for valuation in adjustment_list:
                    value = 0.0
                    if valuation.get('cost_line_id') and valuation.get('cost_line_id') == line.id:
                        if line.split_method == 'by_quantity' and total_qty:
                            per_unit = (line.amount / total_qty)
                            value = valuation.get('quantity') * per_unit
                        elif line.split_method == 'by_weight' and total_weight:
                            per_unit = (line.amount / total_weight)
                            value = valuation.get('weight') * per_unit
                        elif line.split_method == 'by_volume' and total_volume:
                            per_unit = (line.amount / total_volume)
                            value = valuation.get('volume') * per_unit
                        elif line.split_method == 'equal':
                            value = (line.amount / total_line)
                        elif line.split_method == 'by_current_cost_price' and total_cost:
                            per_unit = (line.amount / total_cost)
                            value = valuation.get('former_cost') * per_unit
                        else:
                            value = (line.amount / total_line)

                        if rounding:
                            value = tools.float_round(value, precision_rounding=rounding, rounding_method='UP')
                            fnc = min if line.amount > 0 else max
                            value = fnc(value, line.amount - value_split)
                            value_split += value
                        if valuation.get('move_id') not in towrite_dict:
                            towrite_dict[valuation.get('move_id')] = value
                        else:
                            towrite_dict[valuation.get('move_id')] += value
        for key, value in towrite_dict.items():
            self.env['stock.move'].browse(key).write({'landed_cost': value})
        return True

    def get_valuation_lines(self):
        """
        This method is used update the value of move lines.
        [If any product has no FIFO Or average costing method it raises the warning.]
        --------------------------------------------------------------------------------
        @param self: object pointer
        :return: lines : move_lines
        """
        self.ensure_one()
        lines = []

        for move in self.move_lines:
            # it doesn't make sense to make a landed cost for a product that isn't set as being valuated in real time at real cost
            if move.product_id.cost_method not in ('fifo', 'average') or move.state == 'cancel' or not move.product_qty:
                continue
            vals = {
                'product_id': move.product_id.id,
                'move_id': move.id,
                'quantity': move.product_qty,
                'former_cost': move.product_cost,
                'weight': move.product_id.weight * move.product_qty,
                'volume': move.product_id.volume * move.product_qty
            }
            lines.append(vals)

        if not lines:
            raise UserError(_("Landed costs can only be applied for products with FIFO or average costing method."))
        return lines

    def action_landed_cost(self):
        """
        This method is used to show the Landed Cost of that specific transfer.
        ----------------------------------------------------------------------
        @param self: object pointer
        """
        return {
            'name': 'Landed Cost',
            'type': 'ir.actions.act_window',
            'res_model': 'stock.landed.cost',
            'view_mode': 'tree,form',
            'view_type': 'form',
            'domain': [('picking_ids', '=', self.id)]
        }
