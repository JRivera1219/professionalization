from odoo import models, fields, api
from odoo.tools.translate import _

class ProfessionalizationSchool(models.Model):
    ''' Defining School Information'''

    _name = 'professionalization.school'
    _description = 'School Information'

    name = fields.Char(string='Name', required=True)
    code = fields.Char('Code')
    description = fields.Text(String='Descripción')
    academy = fields.Boolean(String='Academy')



    class HrAcademicFormationCatalogs(models.Model):
        _name = 'hr.academic.formation.catalogs'

        name = fields.Char('name')
        type = fields.Selection([('class', 'Class'),
                                  ('category','Category'),
                                  ('generation','Generation'),
                                  ('group','Group'),
                                  ('funds','Funds'),
                                  ('headquarters','Headquarters'),
                                  ('format','Format')], 'Type', required=True,  defaulf=lambda self: self._context.get('type','type'))



        def _type_default(self, cr, uid, context=None):
            if context is None:
                context = {}
            if 'type' in context:
                return context.get('type', False)
            return False
        _defaults = {
            'type': _type_default,
        }

    class HrAcademicFormationClass(models.Model):

        _name = 'hr.academic.formation.class'

        name = fields.Char('Name')
        code = fields.Char('Code')
        active = fields.Boolean('Active')
        description = fields.Text('Description')

    class HrAcademicFormationCategory(models.Model):

        _name = 'hr.academic.formation.category'

        name = fields.Char('Name')
        code = fields.Char('Code')
        active = fields.Boolean('Active')
        description = fields.Text('Description')

    class HrAcademicFormationBackground(models.Model):

        _name = 'hr.academic.formation.background'

        name = fields.Char('Name')
        code = fields.Char('Code')
        active = fields.Boolean('Active')
        description = fields.Text('Description')

    class HrAcademicFormationFunds(models.Model):

        _name = 'hr.academic.formation.funds'

        name = fields.Char('Name')
        code = fields.Char('Code')
        active = fields.Boolean('Active')
        description = fields.Text('Description')

    class CheckListcourse(models.Model):
        _name = 'hr.check.list.course'
        _rec_name = 'line_name'

        line_name = fields.Char(string='Course Name', required=True)
        code = fields.Char(string='code')
        description = fields.Text(string='Description')


    class HrAcademicFormationFormat(models.Model):

        _name = 'hr.academic.formation.format'

        name = fields.Char('Name')
        code = fields.Char('Code')
        active = fields.Boolean('Active')
        description = fields.Text('Description')

class HrAcademicFormation(models.Model):
    
    _name = 'hr.academic.formation'
    _inherit = 'mail.thread'


    name = fields.Char('name')
    formation_type = fields.Selection([('initial','Initial'),('continuous','Continuous'),('mandos','Mandos'),('docentes','Docentes'),('evaluaciones','Evaluaciones'),('prompcion','Promocion')], 'Formation', required=True)
    type = fields.Selection([('optional','Optional'),('obligatory','Obligatory')], 'Type', required=True)
    institution_id = fields.Many2one('professionalization.school', 'school', required=True)
    institution_name = fields.Char('School Name', related='institution_id.name',store=True)
    description =  fields.Text('Description')
    periodic = fields.Boolean('Periodic')
    annual = fields.Boolean('Annual Cert.')
    first = fields.Integer('First', help='First evaluation period after admission in months')
    frecuency = fields.Integer('Frecuency', help='The amount of mouth after last evaluation to repeat the course')
    class_id = fields.Many2one('hr.academic.formation.class','Class', required=True)
    category = fields.Many2one('hr.academic.formation.category','category', required=True)
    check_list_course_id = fields.Many2many('hr.check.list.course', 'check_list_course_rel', string='list Course')

##09/11/2022
    department = fields.Many2one('hr.department', string='Department', related='employee_name.department_id')
    #date = fields.Datetime(string="Date")
    responsible_user = fields.Many2one('res.users', string='Responsable')
    employee_name = fields.Many2one('hr.employee', string='Employee', size=32)
    employee_company = fields.Many2one('res.company', string='Company', required=True,
                                       default=lambda self: self.env.user.company_id)
    
    
    orientation_id = fields.Many2one('orientation.checklist', string='Orientation Checklist',
                                     domain="[('checklist_department','=', department)]")
    
    orientation_request = fields.One2many('orientation.request', 'request_orientation', string='Orientation Request')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirmed'),
        ('cancel', 'Canceled'),
        ('complete', 'Completed'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    _defaults = {
        'formation_type': 'initial',
        'type': 'obligatory',
    }

    def confirm_orientation(self):
            self.write({'state': 'confirm'})
            for values in self.orientation_id.checklist_line_id:
                self.env['orientation.request'].create({
                'request_name': values.line_name,
                'request_orientation': self.id,
                'partner_id': values.responsible_user.id,
                'request_date': self.date,
                'employee_id': self.employee_name.id,
            })

    def cancel_orientation(self):
        for request in self.orientation_request:
            request.state = 'cancel'
        self.write({'state': 'cancel'})

    def complete_orientation(self):
        force_complete = False
        for request in self.orientation_request:
            if request.state == 'new':
                force_complete = True
        if force_complete:
            return {
                'name': 'Complete Orientation',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'orientation.force.complete',
                'type': 'ir.actions.act_window',
                'context': {'default_orientation_id': self.id},
                'target': 'new',
            }
        self.write({'state': 'complete'})

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.academic.formation')
        result = super(HrAcademicFormation, self).create(vals)
        return result



