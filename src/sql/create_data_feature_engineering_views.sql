-- ============================= CLIENT VIEW =============================

DROP VIEW IF EXISTS client_birth_decade_view;
CREATE VIEW client_birth_decade_view AS
    SELECT id, districtId, (substr(birthNumber, 1, 1) || '0') AS birth_decade from client;

DROP VIEW IF EXISTS client_birth_year_view;
CREATE VIEW client_birth_year_view AS
    SELECT id, districtId, substr(birthNumber, 1, 2) AS birth_year from client;

DROP VIEW IF EXISTS client_view;
CREATE VIEW client_view AS 
SELECT * FROM client_di_view;

-- ============================= ACCOUNT VIEW =============================

DROP VIEW IF EXISTS shared_account_view;
CREATE VIEW shared_account_view AS
SELECT id, COUNT(*) > 1 AS is_shared 
FROM disp 
GROUP BY accountId;

DROP VIEW IF EXISTS account_balance_view;
CREATE VIEW account_balance_view AS
SELECT A.accountId AS id, A.balance
FROM transDev AS A LEFT OUTER JOIN transDev AS B
    ON A.accountId = B.accountId AND A.date < B.date
WHERE B.accountId IS NULL;

DROP VIEW IF EXISTS account_view;
CREATE VIEW account_view AS
SELECT account_di_view.id, districtId, frequency, date, is_shared, balance
FROM account_di_view
    JOIN shared_account_view ON account_di_view.id = shared_account_view.id
    JOIN account_balance_view ON account_di_view.id = account_balance_view.id;

-- ============================= DISP VIEW =============================

DROP VIEW IF EXISTS disp_view;
CREATE VIEW disp_view AS 
SELECT * FROM disp_di_view;

-- ============================= DISTRICT VIEW =============================

DROP VIEW IF EXISTS district_view;
CREATE VIEW district_view AS 
SELECT * FROM district_di_view;

-- ============================= CARD_DEV VIEW =============================

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
SELECT loanDev.id, averageSalary, (amount*1.0 / averageSalary) as ratio
    FROM loanDev JOIN (
        SELECT averageSalary, account.id
        FROM account JOIN district
        WHERE account.districtId = district.id
    ) AS account
    WHERE loanDev.accountId = account.id;

DROP VIEW IF EXISTS loanDev_view;
CREATE VIEW loanDev_view AS
SELECT loanDev_di_view.id, accountId, date, duration, payments, amount, averageSalary, ratio, status
FROM loanDev_di_view JOIN loanAmount_avgSalary_ratio_view
WHERE loanDev_di_view.id = loanAmount_avgSalary_ratio_view.id;