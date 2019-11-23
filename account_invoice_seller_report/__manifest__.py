{
    'name': "Account Invoice Seller Report",

    'summary': """
        Account Invoice Seller Report
        """,

    'category': 'account_invoicing',
    'version': '11.0.1',

    'depends': [
        'account',
        'sale_premiumpaint',
        'account_premiumpaint',
    ],

    'data': [
        'report/report.xml',
        'report/report_invoiceseller.xml',
        'wizard/invoiceseller_report.xml',
    ],

    'installable': True,
    'auto_install': False,
    'application': False,
}
