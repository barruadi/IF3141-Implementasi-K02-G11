# -*- coding: utf-8 -*-
from odoo import models, fields, api


class TransactionEcoethno(models.Model):
    _name = 'transaksi.transaksi'
    _description = 'Transaksi Ecoethno'
    _rec_name = 'no_transaksi'
    _sql_constraints = [
        ('no_transaksi_uniq', 'unique(no_transaksi)', 'Nomor transaksi harus unik.')
    ]

    # Field Utama
    no_transaksi = fields.Char(
        string='No. Transaksi',
        required=True,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('transaksi.transaksi') or 'TRANS/000000'
    )
    
    tanggal_transaksi = fields.Date(
        string='Tanggal Transaksi',
        required=True,
        default=fields.Date.today
    )
    
    # =============================================
    # Relasi dengan Reservasi (FK sesuai ERD D-04)
    # =============================================
    reservasi_id = fields.Many2one(
        'reservasi.reservasi',
        string='Reservasi',
        required=True,
        domain="[('status_reservasi', 'in', ['confirmed', 'done'])]",
        help='Pilih reservasi yang akan dicatat transaksinya'
    )
    
    # =============================================
    # Related Fields (otomatis dari Reservasi)
    # =============================================
    customer_id = fields.Many2one(
        'res.partner',
        string='Pelanggan',
        related='reservasi_id.customer_id',
        store=True,
        readonly=True,
        help='Pelanggan dari reservasi terkait'
    )
    
    customer_name = fields.Char(
        string='Nama Pelanggan',
        related='customer_id.name',
        readonly=True,
        store=True
    )
    
    customer_phone = fields.Char(
        string='No. Kontak Pelanggan',
        related='customer_id.phone',
        readonly=True,
        store=True
    )
    
    tanggal_kegiatan = fields.Date(
        string='Tanggal Kegiatan',
        related='reservasi_id.tanggal_kunjungan',
        store=True,
        readonly=True,
        help='Tanggal kunjungan dari reservasi terkait'
    )
    
    jumlah_peserta = fields.Integer(
        string='Jumlah Peserta',
        related='reservasi_id.jumlah_peserta',
        store=True,
        readonly=True,
        help='Jumlah peserta dari reservasi terkait'
    )
    
    platform_pemesanan = fields.Selection(
        related='reservasi_id.platform_pemesanan',
        string='Platform Pemesanan',
        store=True,
        readonly=True,
        help='Platform pemesanan dari reservasi terkait'
    )

    # =============================================
    # Data Keuangan Transaksi
    # =============================================
    currency_id = fields.Many2one(
        'res.currency',
        string='Mata Uang',
        default=lambda self: self.env.company.currency_id,
        required=True,
        readonly=True,
        help='Mata uang transaksi'
    )
    
    harga_satuan = fields.Monetary(
        string='Harga Satuan (per peserta)',
        currency_field='currency_id',
        required=True,
        default=0.0,
        help='Harga per peserta'
    )
    
    nilai_transaksi = fields.Monetary(
        string='Nilai Transaksi (Rp)',
        currency_field='currency_id',
        compute='_compute_nilai_transaksi',
        store=True,
        readonly=True,
        help='Nilai total transaksi = Harga Satuan × Jumlah Peserta'
    )
    
    # Status Pembayaran
    status_pembayaran = fields.Selection(
        selection=[
            ('belum_bayar', 'Belum Dibayar'),
            ('sebagian', 'Sebagian Dibayar'),
            ('lunas', 'Lunas'),
            ('dibatalkan', 'Dibatalkan'),
        ],
        string='Status Pembayaran',
        default='belum_bayar',
        required=True,
        help='Status pembayaran transaksi'
    )
    
    tanggal_pembayaran = fields.Date(
        string='Tanggal Pembayaran',
        help='Tanggal pembayaran transaksi dikonfirmasi'
    )
    
    metode_pembayaran = fields.Selection(
        selection=[
            ('cash', 'Tunai'),
            ('transfer_bank', 'Transfer Bank'),
            ('kartu_kredit', 'Kartu Kredit'),
            ('e_wallet', 'E-Wallet'),
            ('cek', 'Cek'),
            ('lainnya', 'Lainnya'),
        ],
        string='Metode Pembayaran',
        help='Cara pembayaran yang digunakan'
    )
    
    # Catatan Tambahan
    catatan = fields.Text(
        string='Catatan',
        help='Catatan tambahan tentang transaksi'
    )
    
    # Audit Trail
    created_at = fields.Datetime(
        string='Dibuat pada',
        readonly=True,
        default=fields.Datetime.now
    )
    
    created_by = fields.Many2one(
        'res.users',
        string='Dibuat oleh',
        readonly=True,
        default=lambda self: self.env.user
    )
    
    updated_at = fields.Datetime(
        string='Diperbarui pada',
        readonly=True,
        default=fields.Datetime.now
    )
    
    updated_by = fields.Many2one(
        'res.users',
        string='Diperbarui oleh',
        readonly=True,
        default=lambda self: self.env.user
    )
    
    # Computed Fields
    @api.depends('harga_satuan', 'jumlah_peserta')
    def _compute_nilai_transaksi(self):
        """Hitung nilai transaksi berdasarkan harga satuan dan jumlah peserta"""
        for record in self:
            record.nilai_transaksi = record.harga_satuan * record.jumlah_peserta
    
    # Lifecycle Methods
    @api.model
    def create(self, vals):
        """Override create untuk mencatat user yang membuat record"""
        vals['created_by'] = self.env.user.id
        vals['updated_by'] = self.env.user.id
        return super().create(vals)
    
    def write(self, vals):
        """Override write untuk mencatat user yang mengupdate record"""
        vals['updated_by'] = self.env.user.id
        vals['updated_at'] = fields.Datetime.now()
        return super().write(vals)


class ReservasiInherit(models.Model):
    """Extend reservasi model to add reverse relation to transaksi"""
    _inherit = 'reservasi.reservasi'

    transaksi_ids = fields.One2many(
        'transaksi.transaksi',
        'reservasi_id',
        string='Transaksi Terkait',
        help='Daftar transaksi yang terkait dengan reservasi ini'
    )

