from openerp import fields, api, models

class ms_poli(models.Model):
    _name = "ptf.poli"
    _description = "Poli"
    
    name = fields.Char('Nama Poli', required=True)
    kode = fields.Char('Kode Poli', required=True, copy=False)
    
    _sql_constraints = [
        ('unique_kode', 'unique(kode)', 'Kode Poli duplicate, mohon cek kembali !'),
    ]
    
    @api.multi
    def name_get(self):
        result = []
        for me in self :
            result.append((me.id, "%s - %s" % (me.kode, me.name)))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name :
            recs = self.search([
                '|',
                ('kode', operator, name),
                ('name', operator, name),
            ] + args, limit=limit)
        else :
            recs = self.search([] + args, limit=limit)
        return recs.name_get()
    
