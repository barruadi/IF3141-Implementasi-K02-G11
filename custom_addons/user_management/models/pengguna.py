# -*- coding: utf-8 -*-
from odoo import models, fields


class PenggunaEcoethno(models.Model):
    _name = 'user_management.pengguna'
    _description = 'Pengguna Sistem Ecoethno'
    _rec_name = 'nama'

    nama = fields.Char(
        string='Nama',
        required=True
    )

    user_id = fields.Many2one(
        'res.users',
        string='Akun Login Odoo',
        required=True
    )

    jabatan = fields.Char(
        string='Jabatan'
    )

    divisi = fields.Char(
        string='Divisi'
    )

    hak_akses = fields.Selection(
        [
            ('admin', 'Admin'),
            ('manager', 'Manager'),
            ('staff', 'Staff'),
        ],
        string='Hak Akses',
        required=True
    )

    status_aktif = fields.Boolean(
        string='Status Aktif',
        default=True
    )

    catatan = fields.Text(
        string='Catatan'
    )