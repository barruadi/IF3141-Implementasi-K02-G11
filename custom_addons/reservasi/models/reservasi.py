# -*- coding: utf-8 -*-
from odoo import models, fields


class Reservasi(models.Model):
    _name = 'reservasi.reservasi'
    _description = 'Reservasi Ecoethno'
    _rec_name = 'nama_reservasi'

    nama_reservasi = fields.Char(
        string='Nama Reservasi',
        required=True
    )

    customer_id = fields.Many2one(
        'res.partner',
        string='Pelanggan'
    )

    tanggal_kunjungan = fields.Date(
        string='Tanggal Kunjungan',
        required=True
    )

    jumlah_peserta = fields.Integer(
        string='Jumlah Peserta',
        required=True,
        default=1
    )

    platform_pemesanan = fields.Selection(
        [
            ('traveloka', 'Traveloka'),
            ('whatsapp', 'WhatsApp'),
            ('website', 'Website'),
            ('langsung', 'Langsung'),
        ],
        string='Platform Pemesanan'
    )

    status_reservasi = fields.Selection(
        [
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status Reservasi',
        default='draft'
    )

    catatan = fields.Text(
        string='Catatan'
    )