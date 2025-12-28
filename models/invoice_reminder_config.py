# -*- coding: utf-8 -*-

from odoo import models, fields


class InvoiceReminderConfig(models.Model):
    _name = "invoice.reminder.config"
    _description = "Configuración de Días de Aviso de Factura por Partner"

    name = fields.Char(string="Nombre", required=True)
    partner_id = fields.Many2one(
        "res.partner", string="Partner", required=True, ondelete="cascade"
    )
    days = fields.Integer(string="Días de Aviso", default=5, required=True)
    active = fields.Boolean(string="Activo", default=True)
