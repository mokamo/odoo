# -*- coding: utf-8 -*-
{
    'name': "Product Tree Color",

    'summary': """
        Product Update in Tree color Based on quantity on hand and least quantity user input""",

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
    'category': 'product',
    'version': '8.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product'],

    # always loaded
    'data': [
        # 'sale_inherit_workflow.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode

}