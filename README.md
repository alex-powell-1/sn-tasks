# Project Name

This project is a comprehensive system for managing various aspects of a retail business, including customer management, reporting, scheduled tasks, and integrations with third-party services like Shopify, and Twilio.


## Key Components

### Configuration

- **[creds.py](creds.py)**: Contains various configuration classes such as `Config`, `API`, `Integrator`, `SQL`, `Company`, `Counterpoint`, `Table`, `Twilio`, `Sheety`, `Shopify`, `Consumer`, `BatchFiles`, `Gmail`, `Reports`, `SMSAutomations`, `Logs`, `Backups`, `Coupon`, and `Marketing`.

### Reporting

- **[reporting/daily_revenue.py](reporting/daily_revenue.py)**: Generates daily revenue reports.
- **[templates/reporting/daily_revenue.html](templates/reporting/daily_revenue.html)**: HTML template for the daily revenue report.

### Scheduled Tasks

- **[scheduled_tasks.py](scheduled_tasks.py)**: Manages scheduled tasks such as generating reports, checking network connectivity, and reassessing tiered pricing.

### Customer Tools

- **[customer_tools/customers.py](customer_tools/customers.py)**: Manages customer-related operations.
- **[customer_tools/merge.py](customer_tools/merge.py)**: Handles merging customer data.
- **[customer_tools/stock_notification.py](customer_tools/stock_notification.py)**: Sends stock notifications to customers.

### SMS

- **[sms/sms_automations.py](sms/sms_automations.py)**: Manages SMS automations.
- **[sms/sms_messages.py](sms/sms_messages.py)**: Handles SMS messages.
- **[sms/sms_queries.py](sms/sms_queries.py)**: Manages SMS-related queries.

### Utilities

- **[utilities.py](utilities.py)**: Contains utility functions used across the project.


## License

This project is licensed under the MIT License.
