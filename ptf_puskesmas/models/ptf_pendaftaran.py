from openerp import api, fields, models
from openerp.exceptions import Warning
import unicodedata

class ptf_pendaftaran(models.Model):
    _name = "ptf.pendaftaran"
    _description = "Pendaftaran"
    _order = "name desc"
    
    name = fields.Char(string='Pendaftaran', default='/')
    state = fields.Selection([
         ('draft','Draft'),
         ('confirm','Confirmed'),
         ('cancel','Cancelled')
    ], string='State', default='draft')
    pasien_id = fields.Many2one('res.partner', domain=[('pasien','=',True)], string='Pasien')
    poli_id = fields.Many2one('ptf.poli', string='Poli yang Dituju')
    tanggal = fields.Datetime(string='Tanggal', default=fields.Datetime.now())
    note = fields.Html(string='Note')
    
    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].get_sequence('Pendaftaran','ptf.pendaftaran','DFT/%(y)s/',5)
        return super(ptf_pendaftaran, self).create(vals)
    
    @api.multi
    def name_get(self):
        result = []
        for me_id in self :
            result.append((me_id.id, "%s - %s" % (me_id.name, me_id.pasien_id.name)))
        return result
    
    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name :
            recs = self.search([
                '|',
                ('pasien_id.name', operator, name),
                ('name', operator, name),
            ] + args, limit=limit)
        else :
            recs = self.search([] + args, limit=limit)
        return recs.name_get()
    
    @api.multi
    def action_confirm(self):
        for me_id in self :
            if me_id.state == 'draft':
                self.env['ptf.pemeriksaan'].create({'pendaftaran_id':me_id.id})
                me_id.write({'state':'confirm'})
    
    @api.multi
    def action_cancel(self):
        for me_id in self :
            pemeriksaan_ids = self.env['ptf.pemeriksaan'].search([
                ('pendaftaran_id','=',me_id.id),
                ('state','!=','cancel')
            ])
            if pemeriksaan_ids :
                pemeriksaan_names = [unicodedata.normalize('NFKD', pemeriksaan.name).encode('ascii','ignore') for pemeriksaan in pemeriksaan_ids]
                raise Warning("Silahkan cancel pemeriksaan %s terlebih dahulu !"%pemeriksaan_names)
            me_id.write({'state':'cancel'})
    
    @api.multi
    def unlink(self):
        for me_id in self :
            if me_id.state != 'draft' :
                raise Warning("Tidak bisa menghapus data pendaftaran yang bukan draft !")
        return super(ptf_pendaftaran, self).unlink()
    
