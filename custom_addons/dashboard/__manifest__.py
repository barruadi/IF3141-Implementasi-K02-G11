# -*- coding: utf-8 -*-
{
    'name': 'Dashboard Ecoethno',
    'summary': 'Dashboard laporan operasional dan inventaris Ecoethno',
    'description': '''
        Modul Dashboard Ecoethno digunakan untuk:
        - Menampilkan ringkasan revenue, transaksi, feedback, dan inventaris
        - Menampilkan tren reservasi dan distribusi kunjungan
        - Menampilkan tabel reservasi terbaru dan stok inventaris
        - Mendukung laporan manajemen berbasis data operasional nyata
    ''',
    'author': 'Kelompok 11 - K02 IF3141',
    'license': 'LGPL-3',
    'category': 'Productivity',
    'version': '1.0',
    'depends': [
        'base',
        'web',
        'spreadsheet_dashboard',
        'inventory',
        'reservasi',
        'transaksi',
        'feedback',
        'user_management',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/spreadsheet_dashboard_menu.xml',
        'views/dashboard_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dashboard/static/src/js/dashboard.js',
            'dashboard/static/src/xml/dashboard.xml',
            'dashboard/static/src/scss/dashboard.scss',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
