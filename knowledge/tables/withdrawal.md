# withdrawal

Table containing payment withdrawals related to orders.

## Important columns
| Column | Description |
|---|---|
| orderid | Order ID |
| amountfromcardinkops | Amount paid by card |
| amountfromcashinkops | Amount paid in cash |
| amountfrombonusesinkops | Amount paid using bonuses |
| cancelled | Whether the withdrawal was cancelled |
| ispaid | Whether the withdrawal was successfully paid |
| withdrawaldatetime | Withdrawal datetime |

## Common filters

Successful paid withdrawal:

```sql
cancelled = false
AND ispaid = true
```

## Common joins

Order:

```sql
withdrawal.orderid = "Order".id
```