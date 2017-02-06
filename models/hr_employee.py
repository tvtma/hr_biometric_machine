# -*- coding: utf-8 -*-

from odoo import models, fields


class HrEmployee(models.Model):
    _name = "hr.employee"
    _inherit = "hr.employee"

    emp_code = fields.Char("Emp Code")
    category = fields.Char("category")

