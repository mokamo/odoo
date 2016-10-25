
# -*- coding: utf-8 -*-
from openerp import models,fields

class ProductProduct(models.Model):
    _inherit = 'product.template'
    least_quantity = fields.Integer(string="Least Quantity", required=False, )

