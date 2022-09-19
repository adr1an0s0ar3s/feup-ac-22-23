.read src/sql/create.sql
.mode csv
.separator ;
.import --skip 1 data/account.csv account
.import --skip 1 data/client.csv client