from odoo import models, fields


class AddDestinationWiz(models.TransientModel):
    _name = 'operation.type.wiz'
    _description = 'operation type wizard'

    warehouse_id = fields.Many2one('stock.warehouse',string='Warehouse')
    picking_type_id = fields.Many2one('stock.picking.type',required=True,string='Operation Type')
    code = fields.Selection([('incoming','Receipt'),('outgoing','Delivery'),('internal','Internal Transfer')])

    def change_picking_type(self):
        for rec in self:
            current_record = self.env['stock.picking'].browse(self._context.get('active_id'))
            current_record.state = 'draft'
            current_record.move_ids_without_package.state = 'draft'
            if current_record.sale_id and rec.warehouse_id:
                current_record.sale_id.warehouse_id = rec.warehouse_id.id
                current_record.sale_id.action_cancel()
                current_record.sale_id.action_draft()
                current_record.sale_id.action_confirm()
            if current_record.purchase_id:
                current_record.purchase_id.button_cancel()
                current_record.purchase_id.button_draft()
                current_record.purchase_id.picking_type_id = rec.picking_type_id
                current_record.purchase_id.button_confirm()