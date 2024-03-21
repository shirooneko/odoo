from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    _order = "date_availability desc"

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Nama properti sudah ada, silahkan gunakan nama lain')
    ]

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if record.selling_price < 1:
                raise ValidationError("Harga jual harus lebih besar dari 0")
            if record.selling_price < record.expected_price:
                raise ValidationError("Harga jual tidak boleh kurang dari harga yang diharapkan")
            
    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for prop in self:
            prop.total_area = prop.living_area + prop.garden_area

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "N"
        else:
            self.garden_area = 0
            self.garden_orientation = False

    name = fields.Char(string="Nama", required=True)
    description = fields.Text(string="Deskripsi", default="Deskripsi Properti")
    postcode = fields.Char(string="Kode Pos")
    date_availability = fields.Date(string="Tanggal Ketersediaan", default=fields.Datetime.now)
    expected_price = fields.Float(string="Harga yang Diharapkan")
    selling_price = fields.Float(string="Harga Jual", default=1000000)
    bedrooms = fields.Integer(string="Jumlah Kamar Tidur")
    living_area = fields.Integer(string="Luas Hunian")
    facades = fields.Integer(string="Jumlah Fasad")
    garage = fields.Boolean(string="Garasi")
    garden = fields.Boolean(string="Taman")
    garden_area = fields.Integer(string="Luas Taman")
    garden_orientation = fields.Selection(
        [("N", "Utara"), ("S", "Selatan"), ("E", "Timur"), ("W", "Barat")],
        string="Garden Orientation",
    )
    last_seen = fields.Datetime(string="Terakhir Dilihat", default=fields.Datetime.now)
    
    user_id = fields.Many2one("res.users", string="Salesman", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", readonly=True, copy=False)
    total_area = fields.Integer(readonly=True, compute="_compute_total_area")
    state = fields.Selection(
        selection=[
            ("new", "Baru"),
            ("ready", "Ready"),
            ("offer_received", "Penawaran Diterima"),
            ("offer_accepted", "Penawaran Diterima"),
            ("sold", "Terjual"),
            ("canceled", "Dibatalkan"),
        ],
        string="Status",
        required=True,
        copy=False,
        default="new",
    )

    def action_sold(self):
        if "canceled" in self.mapped("state"):
            raise UserError("Properti yang dibatalkan tidak dapat dijual.")
        return self.write({"state": "sold"})

    def action_cancel(self):
        if "sold" in self.mapped("state"):
            raise UserError("Properti yang terjual tidak dapat dibatalkan.")
        return self.write({"state": "canceled"})
    
    @api.model
    def create(self, vals):
        if vals.get("selling_price") and vals.get("date_availability"):
            vals["state"] = "ready"
        return super().create(vals)

    def unlink(self):
        if not set(self.mapped("state")) <= {"new", "canceled"}:
            raise UserError("Hanya properti dengan status baru dan dibatalkan yang dapat dihapus.")
        return super().unlink()
