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

DROP VIEW IF EXISTS client_view;
CREATE VIEW client_view AS 
SELECT * FROM client_di_view;

-- ============================= ACCOUNT VIEW =============================

DROP VIEW IF EXISTS sharedAccount_view;
CREATE VIEW sharedAccount_view AS
SELECT accountId AS id, COUNT(*) > 1 AS isShared 
FROM disp 
GROUP BY accountId;

-- TODO: remove dependency on loanDev
DROP VIEW IF EXISTS accountBalance_view;
CREATE VIEW accountBalance_view AS
SELECT accountId AS id, balance
FROM transDev JOIN (
    SELECT A.accountId, MAX(A.date) AS lastTransDate
    FROM transDev AS A JOIN loanDev AS B USING (accountId)
    WHERE A.date <= B.date
    GROUP BY A.accountId
) USING (accountId)
WHERE date = lastTransDate
GROUP BY accountId
HAVING MAX(id);

DROP VIEW IF EXISTS medianAmount_view;
CREATE VIEW medianAmount_view AS
SELECT accountId AS id, 
    CASE WHEN count%2=0 THEN
        0.5 * substr(string_list, middle-10, 10) + 0.5 * substr(string_list, middle, 10)
    ELSE
        1.0 * substr(string_list, middle, 10)
    END AS medianAmount
FROM (
    SELECT accountId, 
        group_concat(value_string,"") AS string_list,
        count() AS count, 
        1 + 10*(count()/2) AS middle
    FROM (
        SELECT accountId, 
            printf('%010d',amount) AS value_string
        FROM [transDev]
        ORDER BY accountId,value_string
    )
    GROUP BY accountId
);

DROP VIEW IF EXISTS sumAllTransactions_view;
CREATE VIEW sumAllTransactions_view AS
SELECT accountId AS id, SUM(amount) AS sumAllTransactions
FROM (
    SELECT id, accountId,
        CASE WHEN type LIKE 'withdrawal%'
        THEN -amount
        ELSE amount
        END AS amount
    FROM transDev
)
GROUP BY accountId;

DROP VIEW IF EXISTS insurancePayments_view;
CREATE VIEW insurancePayments_view AS
SELECT accountId AS id, COUNT(*) AS insurancePaymentsCount, AVG(amount) AS insurancePaymentsAverage
FROM transDev
WHERE k_symbol='insurrance payment'
GROUP BY accountId;

DROP VIEW IF EXISTS timesIntoNegativeBalance_view;
CREATE VIEW timesIntoNegativeBalance_view AS
SELECT accountId AS id, COUNT(*) AS timesIntoNegativeBalance
FROM transDev
WHERE balance < 0 AND balance + amount >= 0 AND type LIKE 'withdrawal%'
GROUP BY accountId;

DROP VIEW IF EXISTS numTransactions_view;
CREATE VIEW numTransactions_view AS
SELECT accountId AS id, COUNT(*) AS numTransactions
FROM transDev
GROUP BY accountId;

DROP VIEW IF EXISTS numTransactionsNegBalance_view;
CREATE VIEW numTransactionsNegBalance_view AS
SELECT accountId AS id, COUNT(*) AS numTransactionsNegBalance
FROM transDev
WHERE balance < 0
GROUP BY accountId;

DROP VIEW IF EXISTS numExternalBankTransactions_view;
CREATE VIEW numExternalBankTransactions_view AS
SELECT accountId AS id, COUNT(*) AS numExternalBankTransactions
FROM transDev
WHERE operation = 'collection from another bank' OR operation = 'remittance to another bank'
GROUP BY accountId;

DROP VIEW IF EXISTS transactionTypeCount_view;
CREATE VIEW transactionTypeCount_view AS
SELECT accountId AS id,
    SUM(CASE WHEN type='withdrawal' THEN 1 ELSE 0 END) AS withdrawalCount,
    SUM(CASE WHEN type='withdrawal in cash' THEN 1 ELSE 0 END) AS cashWithdrawalCount,
    SUM(CASE WHEN type='withdrawal' OR type='withdrawal in cash' THEN 1 ELSE 0 END) AS withdrawalAnyMethodCount,
    SUM(CASE WHEN type='credit' THEN 1 ELSE 0 END) AS creditCount
FROM transDev
GROUP BY accountId;

DROP VIEW IF EXISTS account_view;
CREATE VIEW account_view AS
SELECT id, districtId, frequency, date, isShared, balance,
    IFNULL(medianAmount, 0) AS medianAmount,
    IFNULL(sumAllTransactions, 0) AS sumAllTransactions,
    IFNULL(insurancePaymentsCount, 0) AS insurancePaymentsCount,
    IFNULL(insurancePaymentsAverage, 0) AS insurancePaymentsAverage,
    IFNULL(timesIntoNegativeBalance, 0) AS timesIntoNegativeBalance,
    IFNULL(numTransactions, 0) AS numTransactions,
    IFNULL(numTransactionsNegBalance, 0) AS numTransactionsNegBalance,
    IFNULL(numExternalBankTransactions, 0) AS numExternalBankTransactions,
    IFNULL(withdrawalCount, 0) AS withdrawalCount,
    IFNULL(cashWithdrawalCount, 0) AS cashWithdrawalCount, 
    IFNULL(withdrawalAnyMethodCount, 0) AS withdrawalAnyMethodCount, 
    IFNULL(creditCount, 0) AS creditCount
FROM account_di_view
    JOIN sharedAccount_view USING (id)
    LEFT OUTER JOIN accountBalance_view USING (id)
    LEFT OUTER JOIN medianAmount_view USING (id)
    LEFT OUTER JOIN sumAllTransactions_view USING (id)
    LEFT OUTER JOIN insurancePayments_view USING (id)
    LEFT OUTER JOIN timesIntoNegativeBalance_view USING (id)
    LEFT OUTER JOIN numTransactions_view USING (id)
    LEFT OUTER JOIN numTransactionsNegBalance_view USING (id)
    LEFT OUTER JOIN numExternalBankTransactions_view USING (id)
    LEFT OUTER JOIN transactionTypeCount_view USING (id);

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

DROP VIEW IF EXISTS transDev_view;
CREATE VIEW transDev_view AS 
SELECT * FROM transDev_di_view;

-- ============================= LOAN_DEV VIEW =============================

DROP VIEW IF EXISTS loanAmount_avgSalary_ratio_view;
CREATE VIEW loanAmount_avgSalary_ratio_view AS
SELECT loanDev.id, (amount*1.0 / averageSalary) AS ratio
    FROM loanDev JOIN (
        SELECT averageSalary, account.id
        FROM account JOIN district
        WHERE account.districtId = district.id
    ) AS account
    WHERE loanDev.accountId = account.id;

DROP VIEW IF EXISTS maxTransactionDistance_view;
CREATE VIEW maxTransactionDistance_view AS
SELECT A.id, maxWithdrawal, MAX(credit) AS maxCredit, (maxWithdrawal+MAX(credit)) AS maxTransactionAmountDistance FROM (
    (SELECT account.id, MAX(withdrawal) AS maxWithdrawal FROM account 
        JOIN (SELECT accountId AS id, amount AS withdrawal FROM transDev WHERE type='withdrawal' or type='withdrawal in cash') AS W on (account.id=W.id)
        GROUP BY (account.id)) AS A
    JOIN
    (SELECT accountId AS id, amount AS credit FROM transDev WHERE type='credit') AS C on (A.id=C.id)
)
GROUP BY (A.id);

DROP VIEW IF EXISTS avgSanctionInterest_view;
CREATE VIEW avgSanctionInterest_view AS
SELECT id, avgSanctionInterest FROM loanDev 
JOIN (
    SELECT accountId, AVG(amount) AS avgSanctionInterest, date FROM transDev WHERE k_symbol='sanction interest if negative balance'
    GROUP BY (accountId)
) AS A ON (loanDev.accountId=A.accountId)
GROUP BY (id)
HAVING (A.date < loanDev.date);

DROP VIEW IF EXISTS sumSanctionInterest_view;
CREATE VIEW sumSanctionInterest_view AS
SELECT id, sumSanctionInterest FROM loanDev 
JOIN (
    SELECT accountId, SUM(amount) AS sumSanctionInterest, date FROM transDev WHERE k_symbol='sanction interest if negative balance'
    GROUP BY (accountId)
) AS A ON (loanDev.accountId=A.accountId)
GROUP BY (id)
HAVING (A.date < loanDev.date);

DROP VIEW IF EXISTS loansWithStableIncome_view;
CREATE VIEW loansWithStableIncome_view AS
SELECT id, TRUE as hasStableIncome
FROM loanDev
WHERE accountId IN (
    SELECT accountId
    FROM transDev 
    WHERE operation='collection from another bank' and transDev.date < loanDev.date
    GROUP BY accountId, amount
    HAVING COUNT(*) > 3
);

DROP VIEW IF EXISTS loanDev_view;
CREATE VIEW loanDev_view AS
SELECT loanDev_di_view.id, accountId, date, duration, payments, amount, ratio,
    IFNULL(maxWithdrawal, 0),
    IFNULL(maxCredit, 0),
    IFNULL(maxTransactionAmountDistance, 0),
    IFNULL(sumSanctionInterest, 0) AS sumSanctionInterest,
    IFNULL(avgSanctionInterest, 0) AS avgSanctionInterest, 
    IFNULL(hasStableIncome, false) AS hasStableIncome, 
    status
FROM 
    loanDev_di_view 
    JOIN loanAmount_avgSalary_ratio_view ON loanDev_di_view.id = loanAmount_avgSalary_ratio_view.id
    LEFT OUTER JOIN maxTransactionDistance_view ON loanDev_di_view.id = maxTransactionDistance_view.id
    LEFT OUTER JOIN sumSanctionInterest_view ON loanDev_di_view.id = sumSanctionInterest_view.id
    LEFT OUTER JOIN avgSanctionInterest_view ON loanDev_di_view.id = avgSanctionInterest_view.id
    LEFT OUTER JOIN loansWithStableIncome_view ON loanDev_di_view.id = loansWithStableIncome_view.id;