# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"
    _name = "partner.reminder"

    # Por defecto en True para que todos reciban correos a menos que los desmarques
    x_recibe_reminder = fields.Boolean(
        string="Recibir Recordatorios de Pago", default=True
    )

    x_invoice_reminder_days = fields.Integer(string="Dias aviso factura", default=5)
