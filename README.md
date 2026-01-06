# Filtro de Recordatorios de Cliente

Este módulo de Odoo añade funcionalidades para la gestión automatizada de recordatorios de facturas de clientes mediante correo electrónico. Permite configurar avisos predeterminados y personalizados por contacto, asegurando que los clientes reciban notificaciones oportunas sobre sus facturas pendientes.

## Características Principales

*   **Envío Automático:** Utiliza una acción planificada (Cron) para comprobar diariamente las facturas que requieren recordatorio.
*   **Configuración por Defecto:** Envía recordatorios automáticos 5 días antes de la fecha de vencimiento para los contactos habilitados que no tengan una configuración específica.
*   **Configuración Personalizada:** Permite definir reglas específicas de días de aviso para cada contacto a través del modelo `invoice.reminder.config`.
*   **Activación por Contacto:** Campo booleano `x_receive_invoice_reminder` en la ficha del contacto (`res.partner`) para habilitar o inhabilitar la recepción de recordatorios.
*   **Plantillas de Correo:** Utiliza plantillas de correo personalizables (`modulo_reminder.email_template_invoice_reminder`) para el envío de los avisos, incluyendo un resumen de las facturas pendientes.

## Configuración

### Habilitar Contactos
Para que un cliente reciba recordatorios:
1.  Vaya a **Contactos**.
2.  Abra la ficha del cliente.
3.  Marque la casilla **Recibe Reminder** (o el nombre técnico `x_receive_invoice_reminder`).
4.  Asegúrese de que el contacto tenga una dirección de correo electrónico válida.

### Definir Reglas Personalizadas
Si desea sobrescribir el comportamiento por defecto (aviso 5 días antes) para un cliente específico:
1.  Acceda al modelo de configuración `invoice.reminder.config` (dependiendo de la vista configurada, puede estar en Contabilidad o Configuración).
2.  Cree un nuevo registro seleccionando el **Partner** y definiendo los **Días de Aviso**.
    *   *Nota: La lógica actual para reglas personalizadas busca facturas vencidas hace X días (según implementación actual `config.days * -1`), mientras que la regla por defecto busca facturas por vencer en 5 días.*

### Acción Planificada
El módulo instala una acción planificada llamada **Invoice Reminder** que se ejecuta diariamente. Puede ajustar la frecuencia o forzar la ejecución manual desde **Ajustes > Técnico > Automatización > Acciones Planificadas**.

## Dependencias
*   `base`
*   `account`
*   `contacts`
*   `mail`
