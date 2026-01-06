{
    "name": "Customer Invoice Reminder",
    "version": "16.0.1.0",
    "category": "Accounting",
    "depends": ["base", "account", "contacts", "mail"],
    "data": [
        "data/mail_template.xml",
        "data/ir_cron.xml",
        "security/ir.model.access.csv",
        "views/invoice_reminder_config_views.xml",
        "views/partner_reminder_views.xml",
        "views/partner_view.xml",
    ],
    "installable": True,
    "application": True,
    "auto_install": False,
}
