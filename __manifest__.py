# -*- coding: utf-8 -*-
{
    'name': "professionalization",

    'summary': """
        Module for the administration of training and professionalization of police institutions.
        You can request training, set up and schedule a training calendar""",

    'description': """
         Module for the administration of training and professionalization of police institutions.
        You can request training, set up and schedule a training calendar
    """,

    'author': "Ing. Bernardino Hernández Hernández",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'hr',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr',
     'hr_employee_relative',
        #'hr_public_security',
        #'oh_employee_documents_expiry',
        #'history_employee_moves',
        #'feature_location',
        ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/professionalization_view.xml',
        'views/checklist_line_course.xml',
        'views/employee_training_program.xml',
        ### se agrega dos
        'views/orientation_request_mail_template.xml',
        'views/print_pack_certificates_template.xml',
        'views/report.xml',
        'views/orientation_checklist.xml',
        'views/orientation_checklist_line.xml',
        'views/orientation_checklists_request.xml',
        'views/Cuip_view.xml',
         'views/Corp_view.xml',
         ### se agrega dos
        'menu/professionalization_menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'images':['static/description/img.png'],
    'installable': True,
    'auto_install': False,
    'application': True
}
