# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FeedbackEcoethno(models.Model):
    _name = 'feedback.feedback'
    _description = 'Feedback Pelanggan Ecoethno'
    _rec_name = 'no_feedback'
    _order = 'tanggal_feedback desc'

    no_feedback = fields.Char(
        string='No. Feedback',
        required=True,
        readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('feedback.feedback') or 'FB/000000'
    )

    reservasi_id = fields.Many2one(
        'reservasi.reservasi',
        string='Reservasi',
        required=True,
        help='Reservasi yang terkait dengan feedback ini'
    )

    customer_id = fields.Many2one(
        'res.partner',
        string='Pelanggan',
        related='reservasi_id.customer_id',
        readonly=True,
        store=True
    )

    customer_name = fields.Char(
        string='Nama Pelanggan',
        related='reservasi_id.customer_id.name',
        readonly=True,
        store=True
    )

    tanggal_kunjungan = fields.Date(
        string='Tanggal Kunjungan',
        related='reservasi_id.tanggal_kunjungan',
        readonly=True,
        store=True
    )

    tanggal_feedback = fields.Date(
        string='Tanggal Feedback',
        required=True,
        default=fields.Date.today
    )

    rating = fields.Selection(
        selection=[
            ('1', '1 - Sangat Tidak Puas'),
            ('2', '2 - Tidak Puas'),
            ('3', '3 - Cukup'),
            ('4', '4 - Puas'),
            ('5', '5 - Sangat Puas'),
        ],
        string='Rating',
        required=True,
        help='Tingkat kepuasan pelanggan (1-5)'
    )

    catatan_feedback = fields.Text(
        string='Catatan Ulasan',
        help='Ulasan detail dari pelanggan'
    )

    # Audit trail
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

    @api.model
    def create(self, vals):
        vals['created_by'] = self.env.user.id
        return super().create(vals)

    @api.constrains('rating')
    def _check_rating(self):
        for record in self:
            if record.rating not in ('1', '2', '3', '4', '5'):
                raise ValidationError('Rating harus bernilai antara 1 hingga 5.')
