# userwcustomerdata

Main customer profile table.

## Important columns

| Column | Description |
|---|---|
| newdriveuserid | Customer ID |
| email | Customer email |
| creationdatetime | Customer registration datetime |
| customersbalance | Current customer bonus balance |
| preferredlanguage | Preferred language |
| driverslicencedate | Driver licence date |
| activecardnumber | Active payment card number/reference |
| appleidfa | Apple advertising identifier |
| androidadvertisingid | Android advertising identifier |
| friendspromocode | Promo/referral code used by the customer |
| ownpromocode | Customer's own referral code |
| tags | Customer tags |
| comment | Customer comment |
| isblocked | Whether the customer is blocked |

## Common joins

Orders:

```sql
userwcustomerdata.newdriveuserid = "Order".customerid
```

Bonus additions:

```sql
userwcustomerdata.newdriveuserid = bonusaddition.userid
```

## Common usage

Registration date:

```sql
creationdatetime
```

Customer email:

```sql
email
```

Customer language:

```sql
LEFT(preferredlanguage, 2)
```

## Device logic

Possible device segmentation can be derived from:

```sql
appleidfa
androidadvertisingid
```

Possible categories:
- iOS
- Android
- Both
- None

## Business notes

- `newdriveuserid` is the main customer identifier used for joins.
- `customersbalance` represents the current customer bonus balance.
- `isblocked = true` means the customer is blocked.
- Do not invent additional customer attributes that are not documented.