from openerp import models

class ir_sequence(models.Model):
    _inherit = 'ir.sequence'
    
    def get_sequence(self, name=False, obj=False, pref=False, padding=6):
        sequence_id = self.env['ir.sequence'].search([
            ('name', '=', name),
            ('code', '=', obj),
            ('prefix', '=', pref)
        ])
        if not sequence_id :
            sequence_id = self.env['ir.sequence'].sudo().create({
                'name': name,
                'code': obj,
                'implementation': 'no_gap',
                'prefix': pref,
                'padding': padding
            })
        return sequence_id.next_by_id()
    
