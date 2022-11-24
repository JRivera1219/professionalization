# -*- coding: utf-8 -*-


from dateutil.relativedelta import relativedelta
from datetime import datetime, timedelta
from odoo import api, fields, models, _

class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    certificates = fields.Boolean(default=True, string="Certificates")


class EmployeeTrainingProgram(models.Model):

    _name = 'employee.training.program'
    #se remplaza   esto program_name por  esto  program_name1
    _rec_name = 'program_name'
    _description = 'Employee Training Program'
    _inherit = 'mail.thread'

    

    program_name = fields.Char(string='Training Program', required=True)
    program_name1 = fields.Many2one('hr.academic.formation', string='Programas de Entrenamiento', required=True)
    program_department = fields.Many2one('hr.department', string='Departmento', domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]")
    # se agrega program_convener
    program_convener = fields.Many2one('res.users', string='Persona Responsable', size=32, required=True)
    training_id = fields.One2many('hr.employee', string = 'Detalles De Empleados', compute='employee_details')
    training_id1 = fields.Many2many('cuip.cuip' ,'id')
    training_id2 =  fields.Many2many('corp.corp')
    

    #fullname = fields.Char("NombreCompleto", related="training_id.fullname")
    #training_id1 = fields.One2many('hr.department', string = 'Departam Details', compute='departament_details')
    note_id = fields.Text('Descripcion')
    description = fields.Text('Descripcion')
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date From')
    user_id = fields.Many2one('res.users', string='users', default=lambda self: self.env.user)
    #company_id = fields.Many2one('res.company', string='Institución Policial', Required=True, defauld=lambda self: self.env.user.company_id)
    #departamento = fields.Many2one('hr.department', string='Departamento',related='nombre_completo.department_id',required=True)
    date_from1 = fields.Datetime(string='Date From')
    date_to1 = fields.Datetime(string='Date From')

    #department_id1 = fields.Many2one('hr.department')
    company_id = fields.Many2one('res.company', string='Compañia', default=lambda self: self.env.company)


    state = fields.Selection([('new','New'),
                              ('confirm','Confirmed'),
                              ('cancel','Canceled'),
                              ('complete','Completed'),
                              ('print','Print'),
                              ], string='Status', readonlu=True, copy=False, index=True, track_visibility='onchange', default='new')

    @api.onchange('program_department')
    def employee_details(self):
        datas = self.env['hr.employee'].search([('department_id', '=', self.program_department.id)])
        self.training_id = datas
    ## nueva frasee##

    ## nueva frasee##
### los  datos  para la  impresion 
    def print_event(self):
        self.ensure_one()
        started_date = datetime.strftime(self.create_date, "%y-%m-%d ")
        duration = (self.write_date - self.create_date).days
        pause = relativedelta(hours=0)
        difference = relativedelta(self.write_date, self.create_date) - pause
        hours = difference.hours
        minutes = difference.minutes
        data = {
            'dept_id': self.program_department.id,
            'program_name': self.program_name,
            'company_name': self.company_id.name,
            'date_to': started_date,
            'duration': duration,
            'hours': hours,
            'minutes': minutes,
            'program_convener':self.program_convener.name
             # se descomenta el program_convener
        }
        return self.env.ref('professionalization.print_pack_certificates').report_action(self, data=data)
    def complete_event(self):
        self.write({
            'state': 'complete'
        })

    def confirm_event(self):
        self.write({
            'state':'confirm'
        })
        

    def cancel_event(self):
        self.write({
            'state':'cancel'
        })

    def confirm_send_mail(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            #professionalization
            template_id = ir_model_data.get_object_reference('hr_academic_formation', 'orientation_training_mailer')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'mail_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update({
            'default_model': 'employee.training.program',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
        })

        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


### 'Crear a un  monstruo  es mi pasion'  + 'Entender a un Compi que va al GYM y  al Dia siguiente Platicando de su rutina no es nada Facil pero hay que  Escucharlo con Amor  JEJE'
### = Como si me Importara 
###  

