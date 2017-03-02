# -*- coding: utf-8 -*-
###############################################################################
#
#    Tech-Receptives Solutions Pvt. Ltd.
#    Csundayyright (C) 2009-TODAY Tech-Receptives(<http://www.techreceptives.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your sundaytion) any later version.
#
#    This program is distributed in the hsundaye that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a csundayy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from odoo import models, fields


class Project(models.Model):
    _name = 'project.project'
    _inherit = 'project.project'

    desc = fields.Text('Description')
    class_id = fields.Many2one('sunday.class', 'Class')
    student_ids = fields.Many2many('sunday.students', string='Students')
    teachers_ids = fields.Many2many('sunday.teachers', string='Teachers')
