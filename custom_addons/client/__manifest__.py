# -*- coding: utf-8 -*-
{
    'name': "Proper Client",

    'summary': "Lorem Ipsum",

    'description': """
ini deskripsi    """,

    'author': "Shirooneko",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Tools',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','crm'],

    # always loaded
    'data': [
    'security/ir.model.access.csv',
    'views/terminate_contract_wizard_views.xml',
    'views/proper_client_view.xml',
    'views/proper_client_action.xml',
    'views/proper_client_state_view.xml',
    'views/proper_client_state_action.xml',
    'views/proper_client_task_template_view.xml',
    'views/proper_client_task_template_action.xml',
    'views/proper_client_stage_view.xml',
    'views/proper_client_stage_action.xml',
    'views/proper_client_crm_action.xml',
    'views/proper_client_menu.xml',
    ]
}

