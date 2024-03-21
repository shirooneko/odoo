# -*- coding: utf-8 -*-
{
    'name': "Task Management",

    'summary': "Modul untuk mengelola daftar tugas dalam Odoo",

    'description': """
Modul ini menyediakan fitur untuk mengelola daftar tugas dalam Odoo. Pengguna dapat membuat, mengedit, dan menandai tugas selesai dalam aplikasi.

Fitur utama:
- Membuat dan mengedit tugas
- Menandai tugas sebagai selesai
- Melacak status tugas dengan mudah    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        # 'views/views.xml',
        'views/todo_view.xml',
        'views/todo_menu.xml',
        'views/todo_form_view.xml',
        # 'views/assets_backend.xml',
    ],
}

