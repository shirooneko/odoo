{
    'name': "Estate property management",
    'version': '1.0',
    'depends': ['base'],
    'author': "Shirooneko",
    'category': 'App',
    'description': """
        Modul ini digunakan untuk mengelola properti yang dimiliki oleh perusahaan sebagai buat belajar odoo
    """,
    'application': True,
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_view.xml',  
        'views/menu.xml'
    ]
}