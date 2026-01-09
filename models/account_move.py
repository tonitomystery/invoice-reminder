# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import timedelta
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    _inherit = "account.move"

    def send_upcoming_reminders_by_partner(self, dry_run=False):
        """
        Solo envía recordatorios a los partners que tienen una configuración activa en invoice.reminder.config.
        Usa el campo days para calcular la fecha de aviso personalizada por partner.
        """
        self = self.with_user(1)
        today = fields.Date.today()
        _logger.info("Starting send_upcoming_reminders_by_partner for date: %s", today)

        configs = self.env["invoice.reminder.config"].search([("active", "=", True)])
        partners_config = set()

        template = self.env.ref(
            "modulo_reminder.email_template_invoice_reminder", raise_if_not_found=False
        )

        for config in configs:
            partner = config.partner_id
            if (
                not partner
                or not partner.x_receive_invoice_reminder
                or not partner.email
            ):
                continue
            partners_config.add(partner.id)
            reminder_date = today + timedelta(days=config.days * -1)

            _logger.info("reminder_date %s", reminder_date)

            invoices = self.search(
                [
                    ("move_type", "=", "out_invoice"),
                    ("state", "=", "posted"),
                    ("payment_state", "in", ["not_paid", "partial"]),
                    ("partner_id", "=", partner.id),
                    ("invoice_date_due", "=", reminder_date),
                ]
            )
            if not invoices:
                continue

            if dry_run:
                continue

            self._send_reminder_with_template(template, partner, invoices)

        self._send_default_reminders(today, partners_config, dry_run)

    def _send_default_reminders(self, today, partners_config, dry_run):
        """
        Envía recordatorios a partners que no tienen configuración personalizada (5 días antes).
        """
        partners = self.env["res.partner"].search(
            [
                ("x_receive_invoice_reminder", "=", True),
                ("email", "!=", False),
                ("id", "not in", list(partners_config)),
            ]
        )
        _logger.info("Found %s customers for default reminders (5 days before)", len(partners))
        
        template = self.env.ref(
            "modulo_reminder.email_template_invoice_reminder", raise_if_not_found=False
        )

        for partner in partners:
            _logger.info("Sending default reminder to partner %s", partner.name)
            reminder_date = today + timedelta(days=5)
            invoices = self.search(
                [
                    ("move_type", "=", "out_invoice"),
                    ("state", "=", "posted"),
                    ("payment_state", "in", ["not_paid", "partial"]),
                    ("partner_id", "=", partner.id),
                    ("invoice_date_due", "=", reminder_date),
                ]
            )
            if not invoices:
                continue

            if dry_run:
                continue

            self._send_reminder_with_template(template, partner, invoices)

    def _send_reminder_with_template(self, template, partner, invoices):
        """
        Método auxiliar para enviar el recordatorio usando una plantilla de correo.
        Permite pasar el contexto necesario para la tabla de facturas.
        """
        if not template:
            return

        total_due = sum(invoices.mapped("amount_residual"))

        ctx = {
            "invoice_ids": invoices.ids,
            "total_due": total_due,
        }

        main_invoice = invoices[0]

        try:
            body_html = template.with_context(**ctx)._render_field(
                "body_html", [main_invoice.id]
            )[main_invoice.id]
            subject = template.with_context(**ctx)._render_field(
                "subject", [main_invoice.id]
            )[main_invoice.id]

            new_msg = partner.message_post(
                body=body_html,
                subject=subject,
                subtype_xmlid="mail.mt_comment",
                message_type="comment",
                partner_ids=[partner.id],
                notify=True,
            )
        except Exception as e:
            _logger.error("Error sending reminder to partner %s: %s", partner.name, e)
            raise Exception(f"Error al enviar mensaje con plantilla: {e}")
