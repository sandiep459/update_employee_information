from odoo import models,fields,_,api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)

class HrEmployeeChange(models.Model):
    _name="hr.employee.change"
    name_id= fields.Many2one("res.users")
    changed_name=fields.Char()

    # temp_private_street=fields.Char('hr.employee',related="name_id.address_home_id", readonly=False,store=True)
    temp_phone=fields.Char()
    # is_admin_employee = fields.Boolean(compute='_compute_is_admin_employee')
    temp_employee_country_id=fields.Many2one('res.country')
    temp_work_phone=fields.Char(string ="Work Phone")
    
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
    state = fields.Selection([
        ('submitted', 'Submitted'),
        ('validated', 'Validated'),
        ('rejected', 'Rejected')
    ], string='Status', required=True, tracking=True, default='submitted')


    
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

        if self.state != 'submitted':
            raise UserError(_("Only submitted requests can be validated."))

        # Search for the employee linked to the user (name_id) if name_id is a res.users
        employee_update = self.env['hr.employee'].search([('user_id', '=', self.name_id.id)], limit=1)

        if employee_update:
            # Send notification email
            self.action_send_email()

            # Update employee fields with temporary data
            employee_update.write({
                'mobile_phone': self.temp_phone,  # Phone number
                'country_id': self.temp_employee_country_id.id,  # Country
                'work_phone': self.temp_work_phone,  # Work phone
                'private_email': self.temp_private_email,  # Private email
                'marital': self.temp_marital,  # Marital status
                'emergency_contact': self.temp_emergency_contact,  # Emergency contact
                'emergency_phone': self.temp_emergency_phone,  # Emergency phone
                'identification_id': self.temp_identification_id,  # Identification
                'passport_id': self.temp_passport_id,  # Passport ID
                'gender': self.temp_gender,  # Gender
                'birthday': self.temp_birthday,  # Birthday
            })

            # Change the state to validated
            self.state = 'validated'

        else:
            raise ValidationError(_("No employee found for this user."))

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

        # Find the email template for rejection
        template = self.env.ref('update_employee_information.mail_template_for_notifying_the_rejection')
        if not template:
            raise UserError("Mail template not found!")

        # Send rejection email without modifying the template
        template.send_mail(self.id, email_values={
            'email_to': self.name_id.work_email,
            'email_from': self.env.user.login
        }, force_send=True)

        # Update state to rejected before unlinking the record
        self.state = 'rejected'

        # Unlink the record after the state is updated
        self.unlink()


            
     
