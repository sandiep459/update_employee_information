from odoo import models,fields,_,api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HrEmployeeChange(models.Model):
    _name="hr.employee.change"
    name_id = fields.Many2one('hr.employee', string="Name", default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1),create=False,edit=True)

    # temp_private_street=fields.Char('hr.employee',related="name_id.address_home_id", readonly=False,store=True)
    temp_phone=fields.Char('hr.employee', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).phone)
    # is_admin_employee = fields.Boolean(compute='_compute_is_admin_employee')
    temp_employee_country_id=fields.Many2one('res.country')
    temp_work_phone=fields.Char('hr.employee',)
    temp_private_email=fields.Char(string="Email")
    temp_marital=fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ], string='Marital Status')
    temp_emergency_contact=fields.Char(string="Emergency Contact Name")
    temp_emergency_phone=fields.Char(string="Emergecny Phone")
    temp_identification_id=fields.Char(string="Identification No")
    temp_passport_id=fields.Char(string="Passport No")
    temp_gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    temp_birthday=fields.Date(string="Date of Birth")
    temp_place_of_birth=fields.Char(string="Country Of Birth")
    # def _compute_is_admin_employee(self):
    #     # admin_group = self.env.ref('update_employee_information.group_administrator_employee')
    #     if self.env.user.has_group('update_employee_information.group_administrator_employee'):
    #         self.is_admin_employee = True
    #     else:
    #         self.is_admin_employee = False

    
    def action_send_email(self):
        self.ensure_one()
        template = self.env.ref('update_employee_information.mail_template_for_admin_to_validate_the_update')
        if not template:
            raise UserError("Mail template not found!")
        for record in self:
            template.write({'email_to':self.name_id.work_email,
                            'email_from':self.env.user.login})
            template.send_mail(record.id, force_send=True)

     
    
    def validate_change_in_information(self):
        self.ensure_one()
        employee_update = self.env['hr.employee'].search([('id', '=', self.name_id.id)],limit=1)
        if employee_update:
            self.action_send_email()

            employee_update.write({
                'mobile_phone':self.temp_phone,
                'country_id':self.temp_employee_country_id,
                'name_id':self.name_id,
                'mobile_phone':self.temp_phone,
                'country_id':self.temp_employee_country_id,
                'work_phone':self.temp_work_phone,
                'private_email':self.temp_private_email,
                'marital':self.temp_marital,
                'emergency_contact':self.temp_emergency_contact,
                'emergency_phone':self.temp_emergency_phone,
                'identification_id':self.temp_identification_id,
                'passport_id':self.temp_passport_id,
                'gender':self.temp_gender,
                'birthday':self.temp_birthday,
             })
        
            for rec in self:
               rec.unlink()
      
            return    
            

        else :
                raise ValidationError(_("No Update Found"))
        
    def submit_action_send_email(self):
        self.ensure_one()
        template = self.env.ref('update_employee_information.mail_template_for_notifying_admin')
        if not template:
            raise UserError("Mail template not found!")
        for record in self:
            groups=self.env['res.groups'].search([('id','=',78)])
            for user in groups.users:
                template.write({'email_to':user.login,
                                'email_from':self.env.user.login})
                template.send_mail(record.id, force_send=True)   
   
    def reject_change_in_information(self):
        self.ensure_one()
        template = self.env.ref('update_employee_information.mail_template_for_notifying_the_rejection')
        if not template:
            raise UserError("Mail template not found!")
        for rec in self:
               rec.unlink()
        for record in self:
            template.write({'email_to':self.name_id.work_email,
                            'email_from':self.env.user.login})
            template.send_mail(record.id, force_send=True)
            
     
