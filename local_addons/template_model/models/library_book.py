# -*- coding: utf-8 -*-
from openerp.exceptions import UserError
import os
from openerp import models, fields, api
from openerp.addons import decimal_precision as dp
from openerp.fields import Date as fDate
from datetime import timedelta as td


class BaseArchive(models.AbstractModel):
    _name = 'base.archive'

    active = fields.Boolean(default=True)

    def do_archive(self):
        for record in self:
            record.active = not record.active


class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Library Book'
    _order = 'date_release desc, name'
    _rec_name = 'short_name'
    _inherit = ['base.archive']

    name = fields.Char('Title', required=True)
    short_name = fields.Char(
        string='Short Title',
        size=100,  # For Char only
        translate=False,  # also for Text fields
    )
    note = fields.Text('Internal Notes')
    state = fields.Selection(
        [('draft', 'Not Available'),
         ('available', 'Available'),
         ('lost', 'Lost')], 'State')
    description = fields.Html(
        string='Description',
        # optional:
        sanitize=True,
        strip_style=False,
        translate=False,
    )
    cover = fields.Binary('Book Cover')
    out_of_print = fields.Boolean('Out of Print?')
    date_release = fields.Date('Release Date')
    date_updated = fields.Datetime('Last Updated')
    pages = fields.Integer(
        string='Number of Pages',
        default=0,
        help='Total book page count',
        groups='base.group_user',
        states={'cancel': [('readonly', True)]},
        copy=True,
        index=False,
        readonly=False,
        required=False,
        company_dependent=False,
    )
    reader_rating = fields.Float(
        'Reader Average Rating',
        (14, 4),  # Optional precision (total, decimals),
    )
    author_ids = fields.Many2many('res.partner', string='Authors')
    cost_price = fields.Float('Book Cost', dp.get_precision('Book Price'))
    currency_id = fields.Many2one('res.currency', string='Currency')
    retail_price = fields.Monetary(
        'Retail Price',
        # optional:
        currency_field='currency_id',
    )
    publisher_id = fields.Many2one(
        'res.partner',
        string='Publisher',
        # optional:
        ondelete='set null',
        context={},
        domain=[],
    )
    publisher_city = fields.Char(
        'Publisher City',
        related='publisher_id.city')
    age_days = fields.Float(
        string='Days Since Release',
        compute='_compute_age',
        inverse='_inverse_age',
        search='_search_age',
        store=False,
        compute_sudo=False, )
    ref_doc_id = fields.Reference(
        selection='_referencable_models',
        string='Reference Document')
    state = fields.Selection(
        [('draft', 'Unavailable'),
         ('available', 'Available'),
         ('borrowed', 'Borrowed'),
         ('lost', 'Lost')], 'State')
    active = fields.Boolean('Active', default=True)
    data = fields.Text('Data')
    manager_remarks = fields.Text('Manager Remarks')

    @api.multi
    def save(self, filename):
        if '/' in filename or '\\' in filename:
            raise UserError ('Illegal filename %s' % filename)
        path = os.path.join('/home/mo/Odoo-Dev/odoo9/Core/logs/exports', filename)
        try:
            with open(path, 'w') as fobj:
                for record in self:
                    fobj.write(record.data)
                    fobj.write('\n')
        except (IOError, OSError) as exc:
            message = 'Unable to save file: %s' % exc
            raise UserError(message)

    _sql_constraints = [
        ('name_uniq',
         'UNIQUE (name)',
         'Book title must be unique.')
    ]

    @api.constrains('date_release')
    def _check_release_date(self):
        for r in self:
            if r.date_release > fields.Date.today():
                raise models.ValidationError(
                    'Release date must be in the past')

    @api.depends('date_release')
    def _compute_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            delta = (fDate.from_string(book.date_release - today))
            book.age_days = delta.days

    def _inverse_age(self):
        today = fDate.from_string(fDate.today())
        for book in self.filtered('date_release'):
            d = td(days=book.age_days) - today
            book.date_release = fDate.to_string(d)

    def _search_age(self, operator, value):
        today = fDate.from_string(fDate.today())
        value_days = td(days=value)
        value_date = fDate.to_string(today - value_days)
        return [('date_release', operator, value_date)]

    @api.model
    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])

    @api.model
    def _referencable_models(self):
        models = self.env['res.request.link'].search([])
        return [(x.object, x.name) for x in models]

    @api.model
    def is_allowed_transition(self, old_state, new_state):
        allowed = [('draft', 'available'),
                   ('available', 'borrowed'),
                   ('borrowed', 'available'),
                   ('available', 'lost'),
                   ('borrowed', 'lost'),
                   ('lost', 'available')]
        return (old_state, new_state) in allowed

    @api.multi
    def change_state(self, new_state):
        for book in self:
            if book.is_allowed_transition(book.state, new_state):
                book.state = new_state
            else:
                continue

    @api.model
    def get_all_library_members(self):
        library_member_model = self.env['library.member']
        return library_member_model.search([])

        # def name_get(self):
        #     result = []
        #     for record in self:
        #         result.append(
        #             (record.id,
        #              u"%s (%s)" % (record.name, record.date_released)))
        #     return result

    @api.model
    @api.returns('self', lambda rec: rec.id)
    def create(self, values):
        if not self.user_has_groups('library.group_library_manager'):
            if 'manager_remarks' in values:
                raise exceptions.UserError(
                    'You are not allowed to modify '
                    'manager_remarks'
                )
        return super(LibraryBook, self).write(values)

    @api.model
    def fields_get(self,
                   allfields=None,
                   write_access=True,
                   attributes=None):
        fields = super(LibraryBook, self).fields_get(
            allfields=allfields,
            write_access=write_access,
            attributes=attributes
        )
        if not self.user_has_groups(
                'library.group_library_manager'):
            if 'manager_remarks' in fields:
                fields['manager_remarks']['readonly'] = True

class ResPartner(models.Model):
    _inherit = 'res.partner'
    _order = 'name'

    book_ids = fields.One2many(
        'library.book', 'publisher_id',
        relation='library_book_res_partner_rel',  # optional
        string='Published Books')
    authored_book_ids = fields.Many2many(
        'library.book', string='Authored Books')
    count_books = fields.Integer(
        'Number of Authored Books',
        compute='_compute_count_books')

    @api.depends('authored_book_ids')
    def _compute_count_books(self):
        for r in self:
            r.count_books = len(r.authored_book_ids)


class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}

    partner_id = fields.Many2one('res.partner', ondelete='cascade')
    date_start = fields.Date('Member Since')
    date_end = fields.Date('Termination Date')
    member_number = fields.Char()
    loan_duration = fields.Integer('Loan duration', default=15, required=True)