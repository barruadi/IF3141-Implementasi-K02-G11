# -*- coding: utf-8 -*-
{
    'name': "Reservasi Ecoethno",

    'summary': 'Modul untuk mengelola reservasi Ecoethno',

    'description': '''
        Modul Reservasi Ecoethno digunakan untuk:
        - Mengelola reservasi pelanggan
        - Menampilkan kalender reservasi
        - Melihat detail reservasi
        - Mengatur status reservasi
        - Melakukan pencarian reservasi
    ''',

    'author': 'Kelompok 11 - K02 IF3141',

    'category': 'Sales',

    'version': '1.0',

    'depends': [
        'base',
        'sale',
        'crm',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/reservasi_forms.xml',
        'views/reservasi_trees.xml',
        'views/reservasi_menus.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
}