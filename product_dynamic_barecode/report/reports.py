# -*- coding: utf-8 -*-

from openerp import models, fields, api


class PrintReport(models.AbstractModel):
    _name = 'report.product_dynamic_barecode.barcode_report'
    @api.multi
    def render_html(self, data):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('product_dynamic_barecode.barcode_report')
        docargs = {
            'doc_ids': self._ids,
            'doc_model': report.model,
            'docs': self,
            'mydocs': data[0],
        }
        return report_obj.render('product_dynamic_barecode.barcode_report', docargs)
