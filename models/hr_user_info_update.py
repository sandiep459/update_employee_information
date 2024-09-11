from odoo import models,fields,api
from odoo.exceptions import UserError, ValidationError

class HrUserInfoChnage(models.Model):
    _name="hr.user.info.update"
    name_id = fields.Many2one('hr.employee', string="Name", default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1),create=False,edit=True)

    # temp_private_street=fields.Char('hr.employee',related="name_id.address_home_id", readonly=False,store=True)
    temp_phone=fields.Char()
    # is_admin_employee = fields.Boolean(compute='_compute_is_admin_employee')
    temp_employee_country_id=fields.Many2one('res.country', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).country_id)
    temp_work_phone=fields.Char('hr.employee',)
    temp_private_email=fields.Char(string="Email")
    temp_marital=fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ],default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).marital)
    temp_emergency_contact=fields.Char('hr.employee',default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).emergency_contact)
    temp_emergency_phone=fields.Char(string="Emergecny Phone")
    temp_identification_id=fields.Char(string="Identification No")
    temp_passport_id=fields.Char(string="Passport No")
    temp_gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).gender)
    temp_birthday=fields.Date(string="Date of Birth")
    temp_place_of_birth=fields.Char(string="Country Of Birth")

    def submit_action_send_email(self):
        self.ensure_one()
        template = self.env.ref('update_employee_information.mail_template_for_notifying_admin')   
        user_update = self.env['hr.employee.change'].search([])
        if user_update:
            user_update.write({
                'name_id':self.name_id,
                'mobile_phone':self.temp_phone,
                'country_id':self.temp_employee_country_id,
                'temp_work_phone':self.temp_work_phone,
                'temp_private_email':self.temp_private_email,
                'temp_marital':self.temp_marital,
                'temp_emergency_contact':self.temp_emergency_contact,
                'temp_emergency_phone':self.temp_emergency_phone,
                'temp_identification_id':self.temp_identification_id,
                'temp_passport_id':self.temp_passport_id,
                'temp_gender':self.temp_gender,
                'temp_birthday':self.temp_birthday,
             })  
            if not template:
             raise UserError("Mail template not found!")
            for record in self:
                groups=self.env['res.groups'].search([('id','=',78)])
                for user in groups.users:
                    template.write({'email_to':user.login,
                                    'email_from':self.env.user.login})
                    template.send_mail(record.id, force_send=True)   
            return         
        else :
                raise ValidationError(_("No Update Found"))    
      
            
            

       
           


