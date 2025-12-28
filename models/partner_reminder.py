# -*- coding: utf-8 -*-
from odoo import models, fields


class PartnerReminder(models.Model):
    _name = "partner.reminder"
    _description = "Partner Reminder"

    name = fields.Char(string="Name", required=True)
