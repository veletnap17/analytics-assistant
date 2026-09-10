# Fleet Rules

The authoritative source for current fleet size is Google Sheets.

Do not calculate the official current fleet size from PostgreSQL tables `car` or `carmodel`.

Use PostgreSQL `car` and `carmodel` only for vehicle-level information such as:
- VIN
- registration number
- model
- mileage
- vehicle metadata

For questions about current fleet size or number of vehicles, use the Google Sheets fleet source.

The fleet sheet contains historical daily fleet values.
Use the latest available row by `Date`.

Current fleet size is stored in the `Total Fleet` column.

## Car models in analytics

Google Sheets is authoritative only for current fleet counts and current fleet composition.

For analytical metrics grouped by car model, such as:
- revenue by model
- rides by model
- users by model
- average revenue by model
- historical model performance

use PostgreSQL.

Vehicle model information for SQL analytics comes from:

`Order -> car -> carmodel`

Use `carmodel.displayname` as the human-readable model name.