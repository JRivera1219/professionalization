from odoo import models, fields, api
from odoo.tools.translate import _

#from datetime import datetime, date
#from odoo import api, fields, models

#class HrEmployee(models.Model):
#   _inherit = 'hr.employee'

class CUIP(models.Model):
    ''' Informacion de Cuip'''
    
    _name = 'cuip.cuip' 
    _description = 'Informacion de Cuip'
    _inherit = 'mail.thread'
   
    num= fields.Many2one('hr.employee', string="Empleado")
    nombre1 = fields.Char("Numero_Empleado",
                                      related="num.employee_number")
    Nombre_Completo= fields.Char("Nombre_completo",related='num.fullname')
    cuip = fields.Char(String='Clave Única de Identificación Oficial',related='num.CUIP')
    Estatus= fields.Selection(selection=[("no","No"),("NOREGISTRADO","NOREGISTRADO")])
    status= fields.Selection(selection=([('Si','Si'),('No','No')]))
    #Estatus = fields.Char(string="Estatus")
    observacion= fields.Char(string='Observacion')


