# -*- coding: utf-8 -*-
{
    'name': 'Library Management',

    'summary': 'Manage library books, members, and loans',

    'description': """
Long description of module's purpose
    """,

    'author': "Shirooneko",
    'website': "https://www.yourcompany.com",

    'category': 'Tools',
    'version': '0.1',

    'depends': ['base'],

    'data': [
    'security/ir.model.access.csv',
    'views/library_book_action.xml',
    'views/library_book_view.xml',
    'views/library_genre_action.xml',
    'views/library_genre_view.xml',
    'views/library_publisher_action.xml',
    'views/library_publisher_view.xml',  # Tambahkan koma di sini
    'views/library_member_action.xml',  
    'views/library_member_view.xml',
    'views/library_book_loan_action.xml',  
    'views/library_book_loan_view.xml',
    'views/library_book_menu.xml', 
],
}