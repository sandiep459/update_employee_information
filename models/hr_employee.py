from odoo import models,api,fields

class HrEmployee(models.Model):
    _inherit="hr.employee"
    is_admin_employee = fields.Boolean(compute='_compute_is_admin_employee')

 
    def _compute_is_admin_employee(self):
        # admin_group = self.env.ref('update_employee_information.group_administrator_employee')
        if self.env.user.has_group('update_employee_information.group_administrator_employee'):
            self.is_admin_employee = True
        else:
            self.is_admin_employee = False
  
    def update_employee(self):
        self.ensure_one()
        return {'type': 'ir.actions.act_window',
                'res_model': 'hr.employee.change',
                'view_type': 'form',
                'view_mode': 'form',
                'target': 'new',
                }