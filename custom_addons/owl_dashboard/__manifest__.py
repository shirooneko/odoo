# -*- coding: utf-8 -*-
{
    'name' : 'Owl Dashbord',
    'version' : '1.0',
    'summary': 'OWL Tutorial Dashboard',
    'sequence': -1,
    'description': """OWL Tutorial Custom Dashboard""",
    'category': 'OWL',
    'depends' : ['base', 'web', 'sale', 'board'],
    'data': [
        'views/sales_dashboard.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl_dashboard/static/src/components/**/*.js',
            'owl_dashboard/static/src/components/**/*.xml',
            'owl_dashboard/static/src/components/**/*.scss',
        ],
    },
}