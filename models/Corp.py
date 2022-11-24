from odoo import models, fields, api
from odoo.tools.translate import _

class CORP(models.Model):
    ''' Informacion de Corp'''

    _name = 'corp.corp'
    _description = 'Informacion de Corp'
    _inherit = 'mail.thread'

    Numero_empleado = fields.Char(string='Numero De Empleado')
    Corp = fields.Char(string='CORP')
    Nombre = fields.Char(string='Nombre')
    Puesto = fields.Char(string="Puesto")
    Estatus1 = fields.Char(String='Estatus')
    Vigencia= fields.Date(string='Vigencia')

    