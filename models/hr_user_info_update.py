from odoo import models,fields,api

class HrUserInfoChnage(models.Model):
    _name="hr.user.info.update"
    name_id = fields.Many2one('hr.employee', string="Name", default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1),create=False,edit=True)

    # temp_private_street=fields.Char('hr.employee',related="name_id.address_home_id", readonly=False,store=True)
    temp_phone=fields.Char('hr.employee', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).phone)
    is_admin_employee = fields.Boolean(compute='_compute_is_admin_employee')
    temp_employee_country_id=fields.Many2one('res.country', default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).country_id)
    temp_work_phone=fields.Char('hr.employee',)
    temp_private_email=fields.char(string="Email")
    temp_marital=fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
    ],default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).marital, string='Marital Status')
    temp_emergency_contact=fields.Char('hr.employee',default=lambda self: self.env['hr.employee'].search([('user_id', '=', self.env.user.id)], limit=1).emergency_contact,string="Emergency Contact Name")
    temp_emergency_phone=fields.Char('hr.employee',string="Emergecny Phone")
    temp_identrification_id=fields.Char(string="Identification No")
    temp_passport_id=fields.char(string="Passport No")
    temp_gender=fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], string='Gender')
    temp_birthday=fields.Date(string="Date of Birth")
    temp_place_of_birth=fields.Char(string="Country Of Birth")


