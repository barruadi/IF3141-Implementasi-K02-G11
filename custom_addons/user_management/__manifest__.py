# -*- coding: utf-8 -*-
{
    'name': "User Management Ecoethno",

    'summary': 'Modul untuk mengelola pengguna dan hak akses Ecoethno',

    'description': '''
        Modul User Management Ecoethno digunakan untuk:
        - Mengelola akun pengguna
        - Mengatur hak akses
        - Mengelola status aktif/nonaktif user
        - Menampilkan data pengguna sistem
    ''',

    'author': 'Kelompok 11 - K02 IF3141',

    'category': 'Administration',

    'version': '1.0',

    'depends': [
        'base',
    ],

    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/pengguna_forms.xml',
        'views/pengguna_trees.xml',
        'views/pengguna_kanban.xml',
        'views/pengguna_menus.xml',
    ],
}