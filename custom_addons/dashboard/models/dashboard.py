# -*- coding: utf-8 -*-
from datetime import datetime, time, timedelta

from dateutil.relativedelta import relativedelta

from odoo import fields, models
from odoo.exceptions import AccessError, UserError


class DashboardEcoethno(models.AbstractModel):
    _name = 'dashboard.ecoethno'
    _description = 'Dashboard Ecoethno'

    _ALLOWED_PERIODS = {'day', 'week', 'month', 'year', 'custom'}

    def get_dashboard_data(self, period='year', date_start=False, date_end=False):
        self._check_dashboard_access()
        start_date, end_date = self._get_period_range(period, date_start, date_end)

        return {
            'period': period if period in self._ALLOWED_PERIODS else 'year',
            'date_start': fields.Date.to_string(start_date),
            'date_end': fields.Date.to_string(end_date),
            'cards': self._get_cards(start_date, end_date),
            'reservation_trend': self._get_reservation_trend(start_date, end_date),
            'visit_distribution': self._get_visit_distribution(start_date, end_date),
            'recent_reservations': self._get_recent_reservations(start_date, end_date),
            'inventory_rows': self._get_inventory_rows(),
        }

    def _check_dashboard_access(self):
        user = self.env.user
        allowed = (
            user.has_group('user_management.group_ecoethno_admin')
            or user.has_group('user_management.group_ecoethno_manager')
            or user.has_group('base.group_erp_manager')
        )
        if not allowed:
            raise AccessError('Anda tidak memiliki hak akses untuk membuka Dashboard Ecoethno.')

    def _get_period_range(self, period, date_start=False, date_end=False):
        today = fields.Date.context_today(self)
        period = period if period in self._ALLOWED_PERIODS else 'year'

        if period == 'custom':
            if not date_start or not date_end:
                raise UserError('Tanggal mulai dan tanggal akhir wajib diisi.')
            start_date = fields.Date.to_date(date_start)
            end_date = fields.Date.to_date(date_end)
        elif period == 'day':
            start_date = end_date = today
        elif period == 'week':
            start_date = today - timedelta(days=today.weekday())
            end_date = start_date + timedelta(days=6)
        elif period == 'month':
            start_date = today.replace(day=1)
            end_date = start_date + relativedelta(months=1, days=-1)
        else:
            start_date = today.replace(month=1, day=1)
            end_date = today.replace(month=12, day=31)

        if start_date > end_date:
            raise UserError('Tanggal mulai tidak boleh lebih besar dari tanggal akhir.')

        return start_date, end_date

    def _date_domain(self, field_name, start_date, end_date):
        return [
            (field_name, '>=', fields.Date.to_string(start_date)),
            (field_name, '<=', fields.Date.to_string(end_date)),
        ]

    def _datetime_day_domain(self, field_name, day):
        start_dt = datetime.combine(day, time.min)
        end_dt = datetime.combine(day, time.max)
        return [
            (field_name, '>=', fields.Datetime.to_string(start_dt)),
            (field_name, '<=', fields.Datetime.to_string(end_dt)),
        ]

    def _get_cards(self, start_date, end_date):
        today = fields.Date.context_today(self)
        transaction_domain = self._date_domain('tanggal_transaksi', start_date, end_date)
        paid_transaction_domain = transaction_domain + [('status_pembayaran', '=', 'lunas')]
        active_transaction_domain = transaction_domain + [('status_pembayaran', '!=', 'dibatalkan')]
        feedback_domain = self._date_domain('tanggal_feedback', start_date, end_date)

        daily_transaction_domain = self._date_domain('tanggal_transaksi', today, today)
        daily_feedback_domain = self._date_domain('tanggal_feedback', today, today)

        revenue_total = self._sum_model(
            'transaksi.transaksi',
            paid_transaction_domain,
            'nilai_transaksi',
        )
        revenue_daily = self._sum_model(
            'transaksi.transaksi',
            daily_transaction_domain + [('status_pembayaran', '=', 'lunas')],
            'nilai_transaksi',
        )
        transactions_total = self.env['transaksi.transaksi'].sudo().search_count(active_transaction_domain)
        transactions_daily = self.env['transaksi.transaksi'].sudo().search_count(
            daily_transaction_domain + [('status_pembayaran', '!=', 'dibatalkan')]
        )
        feedback_total = self.env['feedback.feedback'].sudo().search_count(feedback_domain)
        feedback_daily = self.env['feedback.feedback'].sudo().search_count(daily_feedback_domain)
        inventory_total = self._get_inventory_total()
        inventory_daily = self._get_inventory_daily(today)

        return [
            {
                'key': 'revenue',
                'label': 'Pendapatan',
                'value': revenue_total,
                'daily_value': revenue_daily,
                'type': 'currency',
            },
            {
                'key': 'transactions',
                'label': 'Transaksi',
                'value': transactions_total,
                'daily_value': transactions_daily,
                'type': 'number',
            },
            {
                'key': 'feedback',
                'label': 'Feedback',
                'value': feedback_total,
                'daily_value': feedback_daily,
                'type': 'number',
            },
            {
                'key': 'inventory',
                'label': 'Inventaris',
                'value': inventory_total,
                'daily_value': inventory_daily,
                'type': 'number',
            },
        ]

    def _sum_model(self, model_name, domain, field_name):
        groups = self.env[model_name].sudo().read_group(domain, [f'{field_name}:sum'], [])
        if not groups:
            return 0
        return groups[0].get(field_name) or 0

    def _get_reservation_trend(self, start_date, end_date):
        groupby, step, key_format, label_format = self._get_trend_bucket_config(start_date, end_date)
        labels = []
        counts = {}
        cursor = self._trend_bucket_start(start_date, groupby)
        final_bucket = self._trend_bucket_start(end_date, groupby)
        while cursor <= final_bucket:
            bucket_key = cursor.strftime(key_format)
            labels.append({
                'key': bucket_key,
                'label': cursor.strftime(label_format),
                'count': 0,
            })
            counts[bucket_key] = 0
            cursor += step

        groups = self.env['reservasi.reservasi'].sudo().read_group(
            self._date_domain('tanggal_kunjungan', start_date, end_date),
            ['tanggal_kunjungan'],
            [f'tanggal_kunjungan:{groupby}'],
        )
        for group in groups:
            range_info = group.get('__range', {}).get(f'tanggal_kunjungan:{groupby}', {})
            range_start = range_info.get('from')
            if not range_start:
                continue
            bucket_key = fields.Date.to_date(range_start).strftime(key_format)
            if bucket_key in counts:
                counts[bucket_key] = self._group_count(group, 'tanggal_kunjungan')

        for item in labels:
            item['count'] = counts[item['key']]
        return labels

    def _get_trend_bucket_config(self, start_date, end_date):
        day_count = (end_date - start_date).days + 1
        if day_count <= 31:
            return 'day', relativedelta(days=1), '%Y-%m-%d', '%d %b'
        if day_count <= 366:
            return 'month', relativedelta(months=1), '%Y-%m', '%b'
        return 'year', relativedelta(years=1), '%Y', '%Y'

    def _trend_bucket_start(self, date_value, groupby):
        if groupby == 'year':
            return date_value.replace(month=1, day=1)
        if groupby == 'month':
            return date_value.replace(day=1)
        return date_value

    def _get_visit_distribution(self, start_date, end_date):
        reservation_model = self.env['reservasi.reservasi'].sudo()
        platform_selection = dict(reservation_model._fields['platform_pemesanan'].selection)
        groups = reservation_model.read_group(
            self._date_domain('tanggal_kunjungan', start_date, end_date),
            ['platform_pemesanan'],
            ['platform_pemesanan'],
        )
        distribution = []
        for group in groups:
            platform = group.get('platform_pemesanan') or 'unknown'
            distribution.append({
                'key': platform,
                'label': platform_selection.get(platform, 'Tidak Diketahui'),
                'value': self._group_count(group, 'platform_pemesanan'),
            })
        return distribution

    def _get_recent_reservations(self, start_date, end_date):
        reservation_model = self.env['reservasi.reservasi'].sudo()
        status_labels = dict(reservation_model._fields['status_reservasi'].selection)
        platform_labels = dict(reservation_model._fields['platform_pemesanan'].selection)
        reservations = reservation_model.search(
            self._date_domain('tanggal_kunjungan', start_date, end_date),
            order='tanggal_kunjungan desc, id desc',
            limit=5,
        )
        rows = []
        for reservation in reservations:
            rows.append({
                'id': reservation.id,
                'name': reservation.nama_reservasi,
                'customer': reservation.customer_id.display_name or '-',
                'visit_date': fields.Date.to_string(reservation.tanggal_kunjungan),
                'participants': reservation.jumlah_peserta,
                'status': reservation.status_reservasi,
                'status_label': status_labels.get(reservation.status_reservasi, '-'),
                'platform': platform_labels.get(reservation.platform_pemesanan, '-'),
                'action': self._record_action('reservasi.reservasi', reservation.id),
            })
        return rows

    def _get_inventory_total(self):
        return self._sum_model('inventory.item', [], 'stocks')

    def _get_inventory_daily(self, today):
        domain = self._datetime_day_domain('write_date', today)
        return self._sum_model('inventory.item', domain, 'stocks')

    def _get_inventory_rows(self):
        items = self.env['inventory.item'].sudo().search([], order='stocks asc, item_id asc')
        rows = []
        for item in items:
            quantity = item.stocks or 0
            rows.append({
                'id': item.id,
                'code': item.item_id,
                'name': item.description,
                'quantity': quantity,
                'status': self._inventory_status(quantity),
                'category': ', '.join(item.category_ids.mapped('name')) or '-',
                'action': self._record_action('inventory.item', item.id),
            })
        return rows

    def _inventory_status(self, quantity):
        if quantity <= 0:
            return 'out'
        if quantity <= 5:
            return 'low'
        return 'available'

    def _record_action(self, model_name, record_id):
        return {
            'type': 'ir.actions.act_window',
            'res_model': model_name,
            'res_id': record_id,
            'views': [[False, 'form']],
            'target': 'current',
        }

    def _group_count(self, group, field_name):
        return group.get('__count') or group.get(f'{field_name}_count') or 0
