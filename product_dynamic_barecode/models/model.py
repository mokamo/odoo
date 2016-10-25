# -*- encoding: utf-8 -*-
from openerp import models, fields, api, _ , exceptions
from openerp.exceptions import Warning, ValidationError
from openerp.tools import float_compare
from dateutil.relativedelta import relativedelta
from datetime import  datetime , date
import openerp.addons.decimal_precision as dp
import logging


class BarcodeReport(models.TransientModel):
    _name = 'barcode.report'
    """Create  Dynamic Barcode For Product"""

    def _get_prod_id(self):
        active_id = self.env.context and self.env.context.get('active_id')
        active_model = self.env.context and self.env.context.get('active_model')
        return active_id

    _description = __doc__
    product_id = fields.Many2one('product.product',string="Product ", required=True,default=_get_prod_id)
    number_of_rows = fields.Integer(string="", required=False, )
    number_of_columns = fields.Integer(string="", required=False, )
    width = fields.Integer(string="", required=False, )
    height = fields.Integer(string="", required=False, )

    @api.multi
    def compute_barcode_data(self):
        arr_product_data=[]
        mydata=[]
        product_obj = self.env['product.product']
        product_data = product_obj.search([('id', '=', self.product_id.id)])
        for my_product_data in product_data:
            arr_product_data.append({
                            'ean13':my_product_data.ean13,
                            'rows':self.number_of_rows,
                            'columns':self.number_of_columns,
                            'product_id':self.product_id.id,
                            'product_name':self.product_id.name,
                            'default_code':self.product_id.default_code,
                            'width':self.width,
                            'height':self.height,
                              })
        mydata.insert(0,arr_product_data)
        return self.env['report'].get_action(self,'product_dynamic_barecode.barcode_report',data=mydata)

