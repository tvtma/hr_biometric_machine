# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DTF
from datetime import datetime, timedelta
from zklib import zklib
import time
from zklib import zkconst


class BiometricMachine(models.Model):
    _name = 'biometric.machine'

    name = fields.Char("Machine IP")
    ref_name = fields.Char("Location")
    port = fields.Integer("Port Number")
    address_id = fields.Many2one("res.partner", 'Working Address')
    company_id = fields.Many2one("res.company", "Company Name")
    atten_ids = fields.One2many('biometric.data', 'machine_id', 'Attendance')

    @api.multi
    def download_attendance(self):
        self.ensure_one()
        machine_ip = self.name
        port = self.port
        zk = zklib.ZKLib(machine_ip, int(port))
        res = zk.connect()
        if res == True:
            zk.enableDevice()
            zk.disableDevice()
            attendance = zk.getAttendance()
            hr_attendance = self.env['hr.attendance']
            hr_employee = self.env['hr.employee']
            biometric_data = self.env['biometric.data']
            if (attendance):
                for lattendance in attendance:
                    time_att = str(lattendance[2].date()) + ' ' + str(lattendance[2].time())
                    atten_time1 = datetime.strptime(str(time_att), DTF)
                    atten_time = atten_time1 - timedelta(hours=5, minutes=30)
                    atten_time = datetime.strftime(atten_time, DTF)
                    atten_time1 = datetime.strftime(atten_time1, DTF)
                    in_time = datetime.strptime(atten_time1, DTF).time()

                    time_new = str(in_time)
                    time_new = time_new.replace(":", ".", 1)
                    time_new = time_new[0:5]
                    print time_att, lattendance[0]
                    try:
                        del_atten_ids = biometric_data.search([('emp_code', '=', str(lattendance[0])), ('name', '=', atten_time)])
                        if del_atten_ids:
                            # hr_attendance.unlink(cr,uid,del_atten_ids)
                            continue
                        else:
                            print "Date %s, Name %s: %s" % (lattendance[2].date(), lattendance[2].time(), lattendance[0])
                            a = biometric_data.create({
                                'name':atten_time,
                                'emp_code':lattendance[0],
                                'machine_id':self.id})
                            print a
                    except Exception, e:
                        pass
                        print "exception..Attendance creation======", e.args
            zk.enableDevice()
            zk.disconnect()
            return True
        else:
            raise ValidationError(_("Unable to connect, please check the parameters and network connections."))

    @api.model
    def schedule_download(self):
        """
        Dowload attendence data regularly
        """
        scheduler_line_obj = self.env['biometric.machine']
        scheduler_line_ids = self.env['biometric.machine'].search([])
        for scheduler_line_id in scheduler_line_ids:
            scheduler_line = scheduler_line_obj.browse(scheduler_line_id)   
            try:
                scheduler_line.download_attendance()
            except:
                raise ValidationError(_('Machine with %s is not connected') % (scheduler_line.name))


    @api.multi
    def clear_attendance(self):
        for machine in self:
            machine_ip = machine.name
            port = machine.port
            zk = zklib.ZKLib(machine_ip, int(port))
            res = zk.connect()
            if res == True:
                zk.enableDevice()
                zk.disableDevice()
                zk.clearAttendance()
                zk.enableDevice()
                zk.disconnect()
                return True
            else:
                raise ValidationError(_("Unable to connect, please check the parameters and network connections."))
