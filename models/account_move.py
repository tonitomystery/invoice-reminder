# -*- coding: utf-8 -*-

from odoo import models, fields
from datetime import timedelta


class AccountMove(models.Model):
    def cron_send_upcoming_reminders(self):
        """
        Método para ejecutar diariamente por el cron y enviar recordatorios agrupados por partner.
        """
        self.send_upcoming_reminders_by_partner(dry_run=False)

    _inherit = "account.move"

    # =========================
    # CRON: PRXIMAS A VENCER
    # =========================
    def send_upcoming_reminders_by_partner(self, dry_run=False):
        """
        Agrupa facturas próximas a vencer por partner y envía recordatorio por el chatter.
        """
        self = self.with_user(1)
        today = fields.Date.today()

        partners = self.env["res.partner"].search(
            [
                ("x_recibe_reminder", "=", True),
                ("email", "!=", False),
            ]
        )

        style_header = (
            "color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;"
        )
        style_table = "width: 100%; border-collapse: collapse; margin-top: 20px; font-family: sans-serif;"
        style_th = "background-color: #f8f9fa; padding: 10px; text-align: left; border-bottom: 2px solid #dee2e6; font-size: 13px;"
        style_td = "padding: 10px; border-bottom: 1px solid #eee; font-size: 13px;"

        for partner in partners:
            days = partner.x_invoice_reminder_days or 5
            target_date = today + timedelta(days=days)

            invoices = self.search(
                [
                    ("move_type", "=", "out_invoice"),
                    ("state", "=", "posted"),
                    ("payment_state", "in", ["not_paid", "partial"]),
                    ("partner_id", "=", partner.id),
                    ("invoice_date_due", "=", target_date),
                ]
            )

            if not invoices:
                continue

            total_due = sum(invoices.mapped("amount_residual"))

            rows = ""
            for inv in invoices:
                ncf = getattr(inv, "l10n_do_fiscal_number", None) or "N/A"
                rows += f"""
                        <tr>
                            <td style=\"{style_td}\"><strong>{inv.name}</strong><br><small style=\"color: #7f8c8d;\">{ncf}</small></td>
                            <td style=\"{style_td}; text-align: center;\">{inv.invoice_date_due}</td>
                            <td style=\"{style_td}; text-align: right;\">{inv.amount_residual:,.2f}</td>
                        </tr>
                    """

            body = f"""
                <div style=\"font-family: Arial, sans-serif; color: #333; max-width: 600px; margin: auto; border: 1px solid #f0f0f0; padding: 20px;\">
                    <h2 style=\"{style_header}\">Aviso de Próximo Vencimiento</h2>
                    <p>Estimado/a <strong>{partner.name}</strong>,</p>
                    <p>Le escribimos para recordarle cordialmente que las siguientes facturas están próximas a vencer:</p>
                    <table style=\"{style_table}\">
                        <thead>
                            <tr>
                                <th style=\"{style_th}\">Documento / NCF</th>
                                <th style=\"{style_th}; text-align: center;\">Vencimiento</th>
                                <th style=\"{style_th}; text-align: right;\">Monto</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows}
                        </tbody>
                    </table>
                    <div style=\"margin-top: 20px; text-align: right; font-size: 1.1em;\">
                        <strong>Total a Pagar: <span style=\"color: #3498db;\">{total_due:,.2f}</span></strong>
                    </div>
                    <p style=\"margin-top: 30px; font-size: 0.9em; color: #555;\">
                        Agradecemos de antemano su gestión de pago para evitar interrupciones en su servicio o cargos por mora.
                    </p>
                    <p style=\"margin-top: 40px; border-top: 1px solid #eee; padding-top: 10px; font-size: 0.85em; color: #95a5a6;\">
                        Atentamente,<br>
                        <strong>Departamento de Administración</strong>
                    </p>
                </div>
                """

            if dry_run:
                print(
                    f" [DRY RUN] Se enviaría aviso preventivo a {partner.email} ({len(invoices)} facturas)."
                )
                continue

            partner.message_post(
                subject="Recordatorio: Facturas Próximas a Vencer",
                body=body,
                message_type="comment",
                subtype_xmlid="mail.mt_comment",
                partner_ids=[partner.id],
            )
