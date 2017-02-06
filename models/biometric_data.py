# -*- coding: utf-8 -*-

from odoo import models, fields

class BiometricData(models.Model):
    _name = "biometric.data"

    name = fields.Datetime('Date')
    emp_code = fields.Char('Employee Code')
    machine_id = fields.Many2one('biometric.machine', 'Mechine No')

