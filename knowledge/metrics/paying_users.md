# Paying Users

A Paying User is a unique customer who completed at least one paid ride during the selected period.

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

## Calculation

Count distinct customers with at least one paid ride during the selected period.

## Example: Paying Users in the last 30 days

```sql
SELECT COUNT(DISTINCT customerid) AS paying_users
FROM "Order"
WHERE totalcostincops > 0
  AND enddatetime >= CURRENT_DATE - INTERVAL '30 days';
```

## Business rules

- Count unique customers, not rides.
- Customer must have at least one paid ride in the selected period.
- Use `enddatetime` for period filtering.
- A customer is counted only once within the selected period.