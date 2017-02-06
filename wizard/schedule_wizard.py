# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ConfigureAttendence(models.TransientModel):
    _name = "configure.attendence"

    @api.model
    def _get_interval_number(self):
        line_id = self.env['ir.cron'].search([('name', 'ilike', 'Download Attendence')])
        return self.env['ir.cron'].browse(line_id).interval_number

    @api.model
    def _get_interval_type(self):
        line_id = self.pool.get('ir.cron').search([('name', 'ilike', 'Download Attendence')])
        return self.pool.get('ir.cron').browse(line_id).interval_type
    
    interval_number = fields.Integer(string="Interval Number", default=_get_interval_number)
    interval_type = fields.Selection([
        ('minutes', 'Minutes'),
        ('hours', 'Hours'),
        ('work_days', 'Work Days'),
        ('days', 'Days'),
        ('weeks', 'Weeks'),
        ('months', 'Months')], string="Interval Unit", default=_get_interval_type)


    @api.multi
    def update_interval(self):
        for line in self:
            interval_number = line.interval_number
            interval_type = line.interval_type

        line_id = self.env['ir.cron'].search([('name', 'ilike', 'Download Attendence')])
        schedule_obj = self.env['ir.cron'].browse(line_id)
        schedule_obj.write({'interval_number': interval_number, 'interval_type':interval_type})
