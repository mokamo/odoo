# -*- coding: utf-8 -*-
{
    'name': "Warehouse updates",

    'summary': """
        Warehouse updtaes""",

    'description': """
        This module make the product row in tree view
        becomes red when the quantity reached the least quantity
        that user input
    """,

    'author': "mohamed.sharafa.mo@gmail.com",
    'website': "https://eg.linkedin.com/in/mohamedsharafmo",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product'],

    # always loaded
    'data': [
        # 'sale_inherit_workflow.xml',
        'templates.xml',
    ],
    # only loaded in demonstration mode

}