# MAU

MAU means Monthly Active Users.

A MAU is a unique customer who completed at least one paid ride during the selected month.

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

Count distinct customers with at least one paid ride in the selected month.

## Example

```sql
SELECT COUNT(DISTINCT customerid) AS mau_users
FROM "Order"
WHERE totalcostincops > 0
  AND enddatetime >= DATE_TRUNC('month', CURRENT_DATE)
  AND enddatetime < DATE_TRUNC('month', CURRENT_DATE) + INTERVAL '1 month';
```

## Business rules

- Count unique customers, not rides.
- Customer must have at least one paid ride in the selected month.
- Use `enddatetime` for the activity period.
- A customer is counted only once per month.