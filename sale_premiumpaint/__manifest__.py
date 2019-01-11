{
    'name': "Sale Stock custom PremiumPaint",

    'summary': """
        Sale Stock custom PremiumPaint""",

    'author': "SimpleIT",
    'website': "http://simpleit.com",

    'category': 'Sale',
    'version': '11.0.1.0',

    'depends': [
        'sales_team',
        'sale_stock',
    ],

    'data': [
        'views/sales_team_view.xml',
        'wizard/sale_daily_report.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
