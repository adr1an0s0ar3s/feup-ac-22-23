# Notes

Medida avaliação competição: AUC

**Tables:**
* LoanDev
* Account
* Client
* Disp
* TransDev
* District
* CardDev

## Loan Table

* Categorical: id, accountId
* Temporal Data: date, duration
* Numerical: amount, payments

Within this table, all accountIds are unique

Amount seems to be within reasonable bounds [49.80€ to 5385.00€]. Currency is unknown, district data should yield more information

Payments range from [319 to 9689], it's the amount paid per month
Example:
|amount |duration| (monthly) payments
| ----- | ----- | --- |
|96396 (963.96€)  | 12| 8033 (80.33€) 

The max amount seems oddly low

The scale might be wrong, I'm still not entirely convinced. A exploration of the transations table is due to fully understand it

The loan year might be important

Totally useless but December seems to be the month with most loans, which is cute
