.read src/sql/create.sql
.mode csv
.separator ;
.import --skip 1 data/district.csv district
.import --skip 1 data/account.csv account
.import --skip 1 data/client.csv client
.import --skip 1 data/disp.csv disp
.import --skip 1 data/card_dev.csv cardDev
.import --skip 1 data/loan_dev.csv loanDev
.import --skip 1 data/trans_dev.csv transDev