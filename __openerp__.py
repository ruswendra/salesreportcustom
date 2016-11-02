# -*- coding: utf-8 -*-
{
    'name': "Sale Report Custom",

    'summary': """
        Report about sales order""",

    'description': """
        Report about sales order
    """,

    'author': "Alisan Catur Adhirajasa",
    'website': "http://www.alisancatur.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Report',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'board','product'],
    "installable":True,
    "auto_install":False,
    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/menu.xml',
        'views/sales_inquiry.xml',
        'views/sales_data.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
