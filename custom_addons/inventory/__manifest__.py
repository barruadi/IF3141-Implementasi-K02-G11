# -*- coding: utf-8 -*-
{
    'name': "Inventory Ecoethno",
    'summary': 'Modul untuk mengelola inventaris barang Ecoethno',
    'description': '''
        Modul Inventory Ecoethno digunakan untuk:
        - Mencatat dan mengelola stok barang
        - Melacak status dan kategori barang
        - Mendukung operasi CRUD inventaris
    ''',
    'author': 'Kelompok 11 - K02 IF3141',
    'category': 'Inventory',
    'version': '1.0',
    'depends': ['base'],
    'data': [
        'data/inventory_sequence.xml',
        'security/ir.model.access.csv',
        'views/inventory_forms.xml',
        'views/inventory_trees.xml',
        'views/inventory_menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory/static/src/js/inventory_list.js',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
