# Order

Main table containing carsharing bookings and rides.

## Important columns
| Column | Description |
|---|---|
| id | Order ID |
| customerid | Customer ID |
| carid | Car ID |
| bookdatetime | Booking datetime |
| rentstartdatetime | Ride start datetime |
| enddatetime | Ride end datetime |
| totalcostincops | Total order cost in cents |
| totalrun | Distance travelled |
| driveminutes | Driving duration in minutes |
| parkminutes | Parking duration in minutes |
| inspectstartdatetime | Inspection start datetime |

## Common rules

Paid ride:
```sql
totalcostincops > 0
```

Started ride:
```sql
rentstartdatetime IS NOT NULL
```

Ride with movement:
```sql
totalrun > 0
```

## Common joins

Customer:
```sql
"Order".customerid = userwcustomerdata.newdriveuserid
```