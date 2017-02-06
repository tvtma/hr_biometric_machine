# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from odoo import tools
from odoo import models, fields, api

class ReportDailyAttendance(models.Model):
    _name = "report.daily.attendance"
    _description = "Daily Attendance Report"
    _order = 'day desc'
    _auto = False
    
    name = fields.Many2one('hr.employee', 'Employee')
    day = fields.Date('Date')
    address_id = fields.Many2one('res.partner', 'Working Address')
    category = fields.Char('category')
    punch = fields.Integer('Number of Punch')
    in_punch = fields.Datetime('In Punch')
    out_punch = fields.Datetime('Out Punch')
    
    
    def _select(self):
        select_str = """
            SELECT
                min(l.id) as id, 
                l.employee_id as name, 
                Count(l.day) as punch, 
                l.day as day,
                l.address_id as address_id,
                l.category as category,
                min(l.name) as in_punch ,
                case when min(l.name) != max(l.name) then max(l.name) end as out_punch
        """
        return select_str
    
    def _from(self):
        from_str = """
            FROM
                hr_attendance AS l
        """
        return from_str
    
    def _join(self):
        join_str = """
        """
        return join_str
    
    def _where(self):
        where_str = """
        """
        return where_str
    
    def _group_by(self):
        group_by_str = """
            GROUP BY 
                employee_id, day, address_id, category
        """
        return group_by_str
    
    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (
            %s
            %s
            %s
            %s
            %s
            )
        """ % (self._table, self._select(), self._from(), self._join(), self._where(), self._group_by()))
        
