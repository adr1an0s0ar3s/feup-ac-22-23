-- LOAN - ACCOUNT 
-- LOAN -- DISPOSITION (OWNER) -- CLIENT
-- ACCOUNT - DISTRICT

-- Number of clients per account (is_shared)
-- Number of cards per account (1 ou 2)
-- ownerCardtype, disponentCardType
-- ownerSex, ownerBirthday
-- all district info about owner
-- latestTransDate, accountBalance, transVolume, sumAllTransAmount (intake-outake)

-- To add: district and transDev
SELECT ownerSex, ownerBirthday, ownerCardType, frequency, account_view.date AS accountCreationDate, isShared, balance, loanDev_view.date AS loanDate, duration as loanDuration, payments as loanPayments, amount as loanAmount, ratio, status
FROM loanDev_view
JOIN account_view ON account_view.id = loanDev_view.accountId
JOIN owners_sex_birthday_view ON owners_sex_birthday_view.accountId = account_view.id
JOIN owners_card_type ON owners_card_type.accountId = account_view.id
LIMIT(5);