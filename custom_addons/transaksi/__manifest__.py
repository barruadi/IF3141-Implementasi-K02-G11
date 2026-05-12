# -*- coding: utf-8 -*-
{
    'name': "Transaksi Ecoethno",
    'summary': 'Modul untuk mengelola riwayat transaksi dan penjualan Ecoethno',
    'description': '''
        Modul Transaksi Ecoethno dirancang untuk:
        - Mencatat dan menyimpan riwayat transaksi pelanggan
        - Menampilkan detail transaksi per pelanggan
        - Mengelola informasi reservasi, paket layanan, dan nilai transaksi
        - Memberikan laporan rekapitulasi transaksi untuk keperluan analisis bisnis
    ''',
    'author': 'Kelompok 11 - K02 IF3141',
    'category': 'Sales',
    'version': '1.0',
    'depends': ['base', 'sale', 'crm', 'reservasi'],
    'data': [
        'security/ir.model.access.csv',
        'data/transaksi_sequence.xml',
        'views/transaksi_menus.xml',
        'views/transaksi_forms.xml',
        'views/transaksi_trees.xml',
        'views/reservasi_form_inherit.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'demo': [
        'data/transaksi_demo.xml',
    ],
}
