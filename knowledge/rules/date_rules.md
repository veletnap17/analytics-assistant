# Date Rules

For ride-based analytics, use `Order.enddatetime` as the default date field.

Examples:
- rides
- FTR
- NTR
- MAU
- paying users
- customer activity

Do not use `bookdatetime` unless the user explicitly asks for booking date.

For revenue and withdrawal-based metrics, use `withdrawal.withdrawaldatetime`.