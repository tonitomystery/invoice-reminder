{
    "name": "Filtro de Recordatorios de Cliente",
    "version": "1.0",
    "category": "Accounting",
    "depends": ["base", "account", "contacts"],
    "data": [
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
