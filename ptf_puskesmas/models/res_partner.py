from openerp import api, fields, models

class res_partner(models.Model):
    _inherit = "res.partner"
    
    dokter = fields.Boolean(string='Dokter')
    pasien = fields.Boolean(string='Pasien')
    kode = fields.Char(string='Kode', default='/')
    name = fields.Char(string='Nama')
    pekerjaan = fields.Selection([
        ('pelajar_mhs','Pelajar/Mahasiswa'),
        ('pegawai_negeri','Pegawai Negeri'),
        ('abri','ABRI'),
        ('swasta','Swasta'),
        ('lain','Lain-Lain'),
    ], string='Pekerjaan')
    nama_pekerjaan = fields.Char('Nama Pekerjaan')
    jenis_kelamin = fields.Selection([('laki','Laki-Laki'),('perempuan','Perempuan')], string='Jenis Kelamin')
    tgl_lahir = fields.Date('Tanggal Lahir')
    gol_darah = fields.Selection([
        ('a','A'),
        ('b','B'),
        ('ab','AB'),
        ('o','O'),
    ], string='Golongan Darah')
    status = fields.Selection([
        ('lajang','Lajang'),
        ('menikah','Menikah'),
        ('duda','Duda'),
        ('janda','Janda'),
    ], string='Status')
    history_pasien = fields.One2many('ptf.pemeriksaan', 'pasien_id', 'History Pasien')
    history_dokter = fields.One2many('ptf.pemeriksaan', 'dokter_id', 'History Dokter')
    
    _sql_constraints = [
        ('unique_kode', 'unique(kode,name)', 'Kombinasi kode dan nama sudah ada, mohon cek kembali !'),
    ]
    
    @api.model
    def create(self, vals):
        if vals.get('pasien', False):
            vals['kode'] = self.env['ir.sequence'].get_sequence('Kode Pasien','res.partner','PSN')
        elif vals.get('dokter', False) and ('kode' not in vals or vals.get('kode', False) == '/'):
            vals['kode'] = self.env['ir.sequence'].get_sequence('Kode Dokter','res.partner','DKT')
        return super(res_partner, self).create(vals)
    
    @api.multi
    def name_get(self):
        result = []
        for me_id in self :
            if me_id.kode and me_id.kode != '/' :
                result.append((me_id.id, "%s - %s" % (me_id.kode, me_id.name)))
            else :
                result.append((me_id.id, me_id.name))
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
