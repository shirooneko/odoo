# -*- coding: utf-8 -*-
{
    'name' : 'OWL Tutorial todo list',
    'version' : '1.0',
    'summary': 'OWL Tutorial',
    'description': """OWL Tutorial""",
    'category': 'OWL',
    'depends' : ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml'
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend': [
            'owl/static/src/components/*/*.js',
            'owl/static/src/components/*/*.xml',
            'owl/static/src/components/*/*.scss',
        ],
    },
}