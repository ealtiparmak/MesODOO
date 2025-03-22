{
    'name': 'BOM Button for Sales Orders',
    'version': '1.0',
    'depends': ['sale', 'mrp'],
    'author': 'Ejder Altiparmak',
    'category': 'Sales',
    'summary': 'Adds a button to fetch BOM components on Sale Orders',
    'installable': True,
    'application': True,
    'auto_install': False,
    'data': [
        'views/sale_order_view.xml',
    ],
}

