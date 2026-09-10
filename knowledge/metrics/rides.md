# Rides

A ride is an order that has been completed and has a positive price.

## Source table

`Order`

## Ride definition

By default, a ride is:

```sql
totalcostincops > 0
AND enddatetime IS NOT NULL
```

## Date field

Use:

```sql
enddatetime
```

Do not use `bookdatetime` unless the user explicitly asks for booking date.

## Calculation

Count rides using:

```sql
COUNT(*)
```

with the ride definition applied.

## Example: rides in the last 30 days

```sql
SELECT COUNT(*) AS rides
FROM "Order"
WHERE totalcostincops > 0
  AND enddatetime IS NOT NULL
  AND enddatetime >= CURRENT_DATE - INTERVAL '30 days';
```

## Business rules

- Use `enddatetime` for ride-based period filtering.
- Only paid rides are counted by default.
- Do not count bookings that were never completed.
- Do not use `bookdatetime` unless explicitly requested.