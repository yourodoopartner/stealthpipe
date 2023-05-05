from odoo import models,fields,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    prepaid_shipping = fields.Float(string='Prepaid Shipping')

    @api.depends('prepaid_shipping', 'order_line')
    def _compute_margin(self):
        """
        overriden _compute_margin method for update the margin
        :param self: object pointer
        """
        res = super(SaleOrder, self)._compute_margin()
        for order in self:
            order.margin = order.margin - order.prepaid_shipping
        return res