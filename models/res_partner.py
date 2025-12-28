# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = "res.partner"

    # Por defecto en True para que todos reciban correos a menos que los desmarques
    x_recibe_reminder = fields.Boolean(
        string="Recibir Recordatorios de Pago", default=True
    )

    invoice_reminder_config_ids = fields.One2many(
        "invoice.reminder.config",
        "partner_id",
        string="Configuraciones de Días de Aviso",
    )
