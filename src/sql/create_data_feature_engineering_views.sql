-- ============================= CLIENT VIEW =============================

DROP VIEW IF EXISTS client_birth_decade_view;
CREATE VIEW client_birth_decade_view AS
    SELECT id, districtId, (substr(birthNumber, 1, 1) || '0') AS birth_decade from client;

DROP VIEW IF EXISTS client_birth_year_view;
CREATE VIEW client_birth_year_view AS
    SELECT id, districtId, substr(birthNumber, 1, 2) AS birth_year from client;

DROP VIEW IF EXISTS owners_sex_birthday_view;
CREATE VIEW owners_sex_birthday_view AS
SELECT accountId, sex AS ownerSex, birthday AS ownerBirthday
FROM disp_view
JOIN client_view ON disp_view.clientId = client_view.id
WHERE type = "OWNER";

DROP VIEW IF EXISTS client_num_transactions;
CREATE VIEW client_num_transactions AS
SELECT clientId, num_transactions
FROM disp
JOIN (
    SELECT accountId, COUNT(*) AS num_transactions
    FROM transDev
    GROUP BY accountId
) AS t ON t.accountId = disp.accountId;

DROP VIEW IF EXISTS client_num_neg_transactions;
CREATE VIEW client_num_neg_transactions AS
SELECT clientId, num_neg_transactions
FROM disp
JOIN (
    SELECT accountId, COUNT(*) AS num_neg_transactions
    FROM transDev
    WHERE balance < 0
    GROUP BY accountId
) AS t ON t.accountId = disp.accountId;

DROP VIEW IF EXISTS client_external_bank_transactions;
CREATE VIEW client_external_bank_transactions AS
SELECT clientId, CASE WHEN t.num_external_bank_transactions IS null THEN 0 ELSE t.num_external_bank_transactions END AS num_external_bank_transactions, t.num_external_bank_transactions IS NOT null AS has_external_bank_transactions
FROM disp
LEFT JOIN (
    SELECT accountId, COUNT(*) AS num_external_bank_transactions
    FROM transDev
    WHERE operation = 'collection from another bank' OR operation = 'remittance to another bank'
    GROUP BY accountId
) AS t ON t.accountId = disp.accountId;

DROP VIEW IF EXISTS client_view;
CREATE VIEW client_view AS 
SELECT * FROM client_di_view;

-- ============================= ACCOUNT VIEW =============================

DROP VIEW IF EXISTS shared_account_view;
CREATE VIEW shared_account_view AS
SELECT accountId as id, COUNT(*) > 1 AS isShared 
FROM disp 
GROUP BY accountId;

DROP VIEW IF EXISTS account_balance_view;
CREATE VIEW account_balance_view AS
SELECT accountId as id, balance
FROM transDev JOIN (
    SELECT A.accountId, MAX(A.date) as lastTransDate
    FROM transDev AS A JOIN loanDev AS B USING (accountId)
    WHERE A.date <= B.date
    GROUP BY A.accountId
) USING (accountId)
WHERE date = lastTransDate
GROUP BY accountId
HAVING MAX(id);

DROP VIEW IF EXISTS account_view;
CREATE VIEW account_view AS
SELECT account_di_view.id, districtId, frequency, date, isShared, balance
FROM account_di_view
    JOIN shared_account_view USING (id)
    LEFT OUTER JOIN account_balance_view USING (id);

-- ============================= DISP VIEW =============================

DROP VIEW IF EXISTS disp_view;
CREATE VIEW disp_view AS 
SELECT * FROM disp_di_view;

-- ============================= DISTRICT VIEW =============================

DROP VIEW IF EXISTS district_view;
CREATE VIEW district_view AS 
SELECT * FROM district_di_view;

-- ============================= CARD_DEV VIEW =============================

DROP VIEW IF EXISTS owners_card_type;
CREATE VIEW owners_card_type AS 
SELECT accountId, cardDev_view.type AS ownerCardType
FROM disp_view
JOIN cardDev_view ON cardDev_view.dispId = disp_view.id
WHERE disp_view.type = "OWNER";

DROP VIEW IF EXISTS disponents_card_type;
CREATE VIEW disponents_card_type AS 
SELECT accountId, cardDev_view.type AS disponentCardType
FROM disp_view
JOIN cardDev_view ON cardDev_view.dispId = disp_view.id
WHERE disp_view.type = "DISPONENT";
-- None exist, interesting

DROP VIEW IF EXISTS cardDev_view;
CREATE VIEW cardDev_view AS 
SELECT * FROM cardDev_di_view;

-- ============================= TRANS_DEV VIEW =============================

-- TODO: Remove leakage
DROP VIEW IF EXISTS maxTransactionDistance_view;
CREATE VIEW maxTransactionDistance AS
SELECT A.id, maxWithdrawal, MAX(credit) as maxCredit, (maxWithdrawal+MAX(credit)) as maxTransactionAmountDistance FROM (
    (SELECT account.id, MAX(withdrawal) as maxWithdrawal FROM account 
        JOIN (SELECT accountId as id, amount as withdrawal FROM transDev WHERE type='withdrawal' or type='withdrawal in cash') as W on (account.id=W.id)
        GROUP BY (account.id)) as A
    JOIN
    (SELECT accountId as id, amount as credit FROM transDev WHERE type='credit') as C on (A.id=C.id)
)
GROUP BY (A.id);

DROP VIEW IF EXISTS avgSanctionInterest_view;
CREATE VIEW avgSanctionInterest_view AS
SELECT id, avgSanctionInterest, status FROM loanDev 
JOIN (
    SELECT accountId, AVG(amount) as avgSanctionInterest, date FROM transDev WHERE k_symbol='sanction interest if negative balance'
    GROUP BY (accountId)
) as A ON (loanDev.accountId=A.accountId)
GROUP BY (id)
HAVING (A.date < loanDev.date);

DROP VIEW IF EXISTS sumSanctionInterest_view;
CREATE VIEW sumSanctionInterest_view AS
SELECT id, sumSanctionInterest, status FROM loanDev 
JOIN (
    SELECT accountId, SUM(amount) as sumSanctionInterest, date FROM transDev WHERE k_symbol='sanction interest if negative balance'
    GROUP BY (accountId)
) as A ON (loanDev.accountId=A.accountId)
GROUP BY (id)
HAVING (A.date < loanDev.date);

DROP VIEW IF EXISTS loansWithStableIncome_view;
CREATE VIEW loansWithStableIncome_view AS
SELECT id, accountId, status FROM loanDev WHERE accountId IN (
    SELECT accountId from (
        SELECT accountId, amount, COUNT(*) as count FROM transDev 
        WHERE operation='collection from another bank' and transDev.date < loanDev.date
        GROUP BY accountId, amount
    ) where count > 3);

DROP VIEW IF EXISTS transDev_view;
CREATE VIEW transDev_view AS 
SELECT * FROM transDev_di_view;

-- ============================= LOAN_DEV VIEW =============================

DROP VIEW IF EXISTS loanAmount_avgSalary_ratio_view;
CREATE VIEW loanAmount_avgSalary_ratio_view AS
SELECT loanDev.id, (amount*1.0 / averageSalary) as ratio
    FROM loanDev JOIN (
        SELECT averageSalary, account.id
        FROM account JOIN district
        WHERE account.districtId = district.id
    ) AS account
    WHERE loanDev.accountId = account.id;

DROP VIEW IF EXISTS loanDev_view;
CREATE VIEW loanDev_view AS
SELECT loanDev_di_view.id, accountId, date, duration, payments, amount, ratio, status
FROM loanDev_di_view JOIN loanAmount_avgSalary_ratio_view
WHERE loanDev_di_view.id = loanAmount_avgSalary_ratio_view.id;