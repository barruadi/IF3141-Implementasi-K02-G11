# -*- coding: utf-8 -*-
{
    'name': "Feedback Ecoethno",
    'summary': 'Modul untuk mengelola feedback dan ulasan pelanggan Ecoethno',
    'description': '''
        Modul Feedback Ecoethno digunakan untuk:
        - Mencatat dan menyimpan feedback pelanggan pasca kunjungan
        - Mengaitkan ulasan dengan data reservasi terkait
        - Menampilkan rekap rating dan catatan ulasan
        - Mendukung evaluasi kualitas layanan
    ''',
    'author': 'Kelompok 11 - K02 IF3141',
    'category': 'Sales',
    'version': '1.0',
    'depends': ['base', 'reservasi'],
    'data': [
        'data/feedback_sequence.xml',
        'security/ir.model.access.csv',
        'views/feedback_forms.xml',
        'views/feedback_trees.xml',
        'views/feedback_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
