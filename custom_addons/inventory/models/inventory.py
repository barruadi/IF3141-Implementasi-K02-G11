# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class InventoryCategory(models.Model):
    _name = 'inventory.category'
    _description = 'Kategori Inventaris'

    name = fields.Char(string='Nama Kategori', required=True)


class InventoryItem(models.Model):
    _name = 'inventory.item'
    _description = 'Barang Inventaris Ecoethno'
    _rec_name = 'item_id'
    _order = 'item_id asc'

    item_id = fields.Char(
        string='ID',
        required=True,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('inventory.item') or 'S-000'
    )

    description = fields.Text(string='Deskripsi', required=True)

    stocks = fields.Integer(string='Stok', default=0)

    status = fields.Selection(
        selection=[
            ('aktif', 'Aktif'),
            ('digunakan', 'Digunakan'),
        ],
        string='Status',
        required=True,
        default='aktif',
    )

    category_ids = fields.Many2many(
        'inventory.category',
        string='Kategori',
    )

    @api.constrains('stocks')
    def _check_stocks(self):
        for record in self:
            if record.stocks < 0:
                raise ValidationError('Stok tidak boleh bernilai negatif.')

    def action_edit(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'inventory.item',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_detail(self):
        view_id = self.env.ref('inventory.inventory_view_form_detail').id
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'inventory.item',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': view_id,
            'target': 'new',
        }

    def action_delete(self):
        self.unlink()
        return {'type': 'ir.actions.act_window_close'}

    def action_save_and_close(self):
        return {'type': 'ir.actions.act_window_close'}
