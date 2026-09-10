# Revenue

Revenue is the total value of successful paid withdrawals excluding bonuses.

## Source table

`withdrawal`

## Calculation

```sql
SUM(amountfromcardinkops + amountfromcashinkops)::numeric / 100.00
```

## Required filters

```sql
cancelled = false
AND ispaid = true
```

## Date

For period filtering use:

```sql
withdrawaldatetime
```

Example:

```sql
withdrawaldatetime >= CURRENT_DATE - INTERVAL '30 days'
```

## Order-level revenue

```sql
SELECT
    w.orderid,
    SUM(w.amountfromcardinkops + w.amountfromcashinkops)::numeric / 100.00 AS revenue
FROM withdrawal w
WHERE w.cancelled = false
  AND w.ispaid = true
GROUP BY w.orderid
```

## Business rules

- Revenue includes only card and cash payments.
- Bonuses must NOT be included in revenue.
- Amounts are stored in cents/kopecks and must be divided by `100.00`.
- Do not use `Order.totalcostincops` as revenue unless explicitly requested.
- Do not infer or display a currency unless explicitly provided.