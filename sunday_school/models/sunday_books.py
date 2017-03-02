# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Copyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import timedelta, date

class SundayTag(models.Model):
    _name = 'sunday.tag'
    _description = 'Tags'

    name = fields.Char('Name', size=64, required=True)
    
class SundayAuthor(models.Model):
    _name = 'sunday.author'
    _description = 'Authors'

    name = fields.Char('Name', size=128, required=True)
    book_ids = fields.Many2many('sunday.book', string='Book(s)')

class SundayPublisher(models.Model):
    _name = 'sunday.publisher'
    _description = 'Publisher'

    name = fields.Char('Name', size=20, required=True)
    book_ids = fields.Many2many('sunday.book', string='Book(s)')

class SundayBook(models.Model):
    _name = 'sunday.book'
    _description = 'Book(s)'
    _inherit = 'mail.thread'


    name = fields.Char('Title', size=128, required=True)
    isbn = fields.Char('ISBN Code', size=64)
    tags = fields.Many2many('sunday.tag', string='Tag(s)')
    author_ids = fields.Many2many('sunday.author', string='Author(s)', required=True)
    edition = fields.Char('Edition')
    description = fields.Text('Description')
    publisher_ids = fields.Many2many('sunday.publisher', string='Publisher(s)', required=True)
    movement_line = fields.One2many('sunday.book.movement', 'book_id', 'Movements')
    queue_ids = fields.One2many('sunday.book.queue', 'book_id', 'Book Queue')

    _sql_constraints = [
        ('unique_name_isbn', 'unique(isbn)', 'ISBN code must be unique per book!'),
    ]
    
class SundayBookQueue(models.Model):
    _name = 'sunday.book.queue'
    _description = 'Book Queue'

    name = fields.Char("Sequence No", readonly=True, copy=False, default='/')
    partner_id = fields.Many2one('res.partner', 'Student/Parent', default=lambda self: self.env.user.partner_id.ids[0])
    book_id = fields.Many2one(
        'sunday.book', 'Book(s)', required=True, track_visibility='onchange')
    date = fields.Date('Date', required=True, default=fields.Date.today(), readonly=True)
    state = fields.Selection(
        [('request', 'Request'), ('accept', 'Accepted')],
        'State', copy=False, default='request', track_visibility='onchange')



    @api.model
    def create(self, vals):
        if vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'sunday.book.queue') or '/'
        return super(SundayBookQueue, self).create(vals)

    @api.one
    def do_accept(self):
        self.state = 'accept'
        self.env['sunday.book.movement'].create({
            'book_id': self.book_id.id,
            'issued_date': fields.Date.today(),
            'partner_id': self.partner_id.id,
            'state': 'issue',
        })

    @api.one
    def do_request_again(self):
        self.state = 'request'

class SundayBookMovement(models.Model):
    _name = 'sunday.book.movement'
    _description = 'Book Movement'
    _rec_name = 'book_id'

    def returned(self):
        self.return_date = fields.Date.today()
        self.state = 'returned'

    book_id = fields.Many2one('sunday.book', 'Book', required=True)
    issued_date = fields.Date('Issued Date', required=True, default=fields.Date.today())
    return_date = fields.Date('Due Date',)
    partner_id = fields.Many2one('res.partner', 'Person', default=lambda self: self.env.uid)
    state = fields.Selection(
        [('reserve', 'Reserved'),
         ('issue', 'Issued'), ('lost', 'Lost'),
         ('returned', 'Returned'), ], 'State',
        default='issue', track_visibility='onchange')

    @api.constrains('issued_date', 'return_date')
    def _check_date(self):
        if self.return_date is not False and self.issued_date > self.return_date:
            raise ValidationError(_(
                'Return Date cannot be set before Issued Date.'))

    @api.onchange('book_unit_id')
    def onchange_book_unit_id(self):
        self.state = self.book_unit_id.state
        self.book_id = self.book_unit_id.book_id

    @api.onchange('library_card_id')
    def onchange_library_card_id(self):
        self.type = self.library_card_id.type
        self.student_id = self.library_card_id.student_id.id
        self.faculty_id = self.library_card_id.faculty_id.id
        self.return_date = date.today() + \
            timedelta(days=self.library_card_id.library_card_type_id.duration)

    @api.one
    def issue_book(self):
        ''' function to issue book '''
        if self.book_unit_id.state and \
                self.book_unit_id.state == 'available':
            self.book_unit_id.state = 'issue'
            self.state = 'issue'

    @api.one
    def return_book(self, return_date):
        if not return_date:
            return_date = fields.Date.today()
        self.state = 'returned'
