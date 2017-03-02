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
from odoo.exceptions import ValidationError


class SundayStudent(models.Model):
    _name = 'sunday.students'
    _description = 'Students'
    _inherits = {'res.partner': 'partner_id'}

    birth_date = fields.Date('Birth Date', required=True)
    gender = fields.Selection(
        [('m', 'Male'), ('f', 'Female'),
         ('o', 'Other')], 'Gender', required=True)
    nationality = fields.Many2one('res.country', 'Nationality')
    parents_ids = fields.Many2many('sunday.parents', string='Parents')
    photo = fields.Binary('Photo')
    partner_id = fields.Many2one(
        'res.partner', 'Partner', required=True, ondelete="cascade")
    gr_no = fields.Char("GR Number", size=20)
    class_id = fields.Many2one('sunday.class', 'Class(es)')
    subject_ids = fields.Many2many('project.project',  string='Subject(s)')

    @api.one
    @api.constrains('birth_date')
    def _check_birthdate(self):
        if self.birth_date > fields.Date.today():
            raise ValidationError(_(
                "Birth Date can't be greater than current date!"))
