# NTR

NTR means Next Time Rider.

An NTR is a returning customer who completed at least one paid ride during the selected period and whose first paid ride happened before that period.

## Source table

`Order`

## Customer identifier

```sql
customerid
```

## Paid ride

```sql
totalcostincops > 0
```

## Date field

Use:

```sql
enddatetime
```

Do not use `bookdatetime` unless the user explicitly asks for booking date.

## Logic

1. Find each customer's first paid ride using `MIN(enddatetime)`.
2. Find customers with at least one paid ride during the selected period.
3. Exclude customers whose first paid ride happened inside the selected period.

## Example: NTR in the last 30 days

```sql
WITH ftr AS (
    SELECT
        customerid,
        MIN(enddatetime) AS ftr_datetime
    FROM "Order"
    WHERE totalcostincops > 0
    GROUP BY customerid
),
active_users AS (
    SELECT DISTINCT customerid
    FROM "Order"
    WHERE totalcostincops > 0
      AND enddatetime >= CURRENT_DATE - INTERVAL '30 days'
)
SELECT COUNT(*) AS ntr_users
FROM active_users a
JOIN ftr f ON a.customerid = f.customerid
WHERE f.ftr_datetime < CURRENT_DATE - INTERVAL '30 days';
```

## Business rules

- Count unique customers, not rides.
- Customer must have at least one paid ride during the selected period.
- Customer's FTR must be before the selected period.
- Customers whose first paid ride occurred during the selected period are FTR, not NTR.
- Use `enddatetime` for ride-based period logic.