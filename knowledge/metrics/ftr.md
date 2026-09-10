# FTR

FTR means First Time Rider.

An FTR is a customer who completed their first paid ride.

## Source table

`Order`

## Customer identifier

Use:

```sql
customerid
```

## FTR definition

For each customer, find the earliest paid ride.

A paid ride is:

```sql
totalcostincops > 0
```

The FTR date is the earliest:

```sql
bookdatetime
```

among paid rides for that customer.

## Example

```sql
SELECT
    customerid,
    MIN(enddatetime) AS ftr_datetime
FROM "Order"
WHERE totalcostincops > 0
GROUP BY customerid
```

## FTR count for a period

To calculate how many customers became FTR during a period:

```sql
WITH ftr AS (
    SELECT
        customerid,
        MIN(enddatetime) AS ftr_datetime
    FROM "Order"
    WHERE totalcostincops > 0
    GROUP BY customerid
)
SELECT COUNT(*) AS ftr_users
FROM ftr
WHERE ftr_datetime >= CURRENT_DATE - INTERVAL '30 days';
```

## Business rules

- Count each customer only once.
- Only paid rides are considered.
- The first paid ride determines the FTR date.
- Do not count later rides as FTR.
- Do not use customer registration date as FTR date.