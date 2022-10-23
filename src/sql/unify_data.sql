-- LOAN - ACCOUNT 
-- LOAN -- DISPOSITION (OWNER) -- CLIENT
-- ACCOUNT - DISTRICT

-- Number of clients per account (is_shared)
-- Number of cards per account (1 ou 2)
-- ownerCardtype, disponentCardType
-- ownerSex, ownerBirthday
-- all district info about owner
-- latestTransDate, accountBalance, transVolume, sumAllTransAmount (intake-outake)

-- To add: and transDev
SELECT ownerSex, ownerBirthday, ownerCardType, frequency, account_view.date AS accountCreationDate, isShared, balance, loanDev_view.date AS loanDate, duration as loanDuration, payments as loanPayments, amount as loanAmount, ratio, districtName, region, nInhabitants, nMunicipalitiesSub499Inhabitants, nMunicipalities500to1999Inhabitants, nMunicipalities2000to9999Inhabitants, nMunicipalitiesOver10000Inhabitants, nCities, urbanInhabitantsRatio, averageSalary, unemploymentRate95, unemploymentRate96, nEnterpreneursPer1000Inhabitants, commitedCrimes95, commitedCrimes96, status
FROM loanDev_view
JOIN account_view ON account_view.id = loanDev_view.accountId
JOIN owners_sex_birthday_view ON owners_sex_birthday_view.accountId = account_view.id
LEFT OUTER JOIN owners_card_type ON owners_card_type.accountId = account_view.id
JOIN district_view ON district_view.id = account_view.districtId;