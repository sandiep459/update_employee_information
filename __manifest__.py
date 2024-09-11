{
    'name': 'Employee Information Update',
    'version': '16.0',
    'summary': 'Employee information Update',
    "description":'''
      Student Profile Management is a robust solution for educational institutions to manage student information. 
    ''',
    "author": "Sandeep Shrestha",
   
   
    
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/employee_mail_template.xml',
        'views/email_template_for_admin.xml',
        'views/hr_employee_change_view.xml',
        'views/inherit_hr_employee_view_form.xml',
        'views/update_rejection_email.xml',
       
    ],
    "depends": ['hr','base'],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
