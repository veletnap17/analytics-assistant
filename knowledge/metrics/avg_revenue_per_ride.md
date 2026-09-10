# Average Revenue per Ride

Average Revenue per Ride is total revenue divided by the number of paid rides in the selected period.

## Revenue source

Use `withdrawal`.

Revenue:

```sql
SUM(amountfromcardinkops + amountfromcashinkops)::numeric / 100.00
```

Required withdrawal filters:

```sql
cancelled = false
AND ispaid = true
```

Use `withdrawaldatetime` for the revenue period.

## Ride source

Use `Order`.

A paid ride is:

```sql
totalcostincops > 0
AND enddatetime IS NOT NULL
```

Use `enddatetime` for ride period filtering.

## Calculation

```text
Average Revenue per Ride = Total Revenue / Paid Rides
```

## Business rules

- Bonuses are not included in revenue.
- Revenue uses `withdrawaldatetime`.
- Rides use `enddatetime`.
- Do not use `Order.totalcostincops` as revenue.