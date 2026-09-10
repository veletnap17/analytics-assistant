# Revenue per User

Revenue per User is total revenue divided by the number of unique paying users in the selected period.

## Revenue

Use `withdrawal`.

```sql
SUM(amountfromcardinkops + amountfromcashinkops)::numeric / 100.00
```

with:

```sql
cancelled = false
AND ispaid = true
```

## Paying users

Use `Order`.

```sql
COUNT(DISTINCT customerid)
```

with:

```sql
totalcostincops > 0
AND enddatetime IS NOT NULL
```

## Calculation

```text
Revenue per User = Total Revenue / Paying Users
```

## Business rules

- Bonuses are not included in revenue.
- Revenue period uses `withdrawaldatetime`.
- Paying-user period uses `enddatetime`.