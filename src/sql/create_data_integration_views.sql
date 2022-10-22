-- ============================= CLIENT VIEW =============================

DROP VIEW IF EXISTS client_di_view;
CREATE VIEW client_di_view AS
SELECT id, districtId, sex,
    CASE WHEN substr(birthNumber,3,2) > '50'
    THEN substr(birthNumber,1,2) || substr('0' || (substr(birthNumber,3,2)-50),-2,2) || substr(birthNumber,5,2)
    ELSE birthNumber
    END AS birthday
FROM (SELECT id, districtId, birthNumber,
        CASE WHEN substr(birthNumber,3,2) > '50'
        THEN 'female'
        ELSE 'male'
        END AS sex
    FROM client);

-- ============================= ACCOUNT VIEW =============================

DROP VIEW IF EXISTS account_di_view;
CREATE VIEW account_di_view AS
SELECT * FROM account;

-- ============================= DISP VIEW =============================

DROP VIEW IF EXISTS disp_di_view;
CREATE VIEW disp_di_view AS
SELECT * FROM disp;

-- ============================= DISTRICT VIEW =============================

DROP VIEW IF EXISTS district_di_view;
CREATE VIEW district_di_view AS
SELECT * FROM district;

-- ============================= CARD_DEV VIEW =============================

DROP VIEW IF EXISTS cardDev_di_view;
CREATE VIEW cardDev_di_view AS
SELECT * FROM cardDev;

-- ============================= TRANS_DEV VIEW =============================

DROP VIEW IF EXISTS transDev_di_view;
CREATE VIEW transDev_di_view AS
SELECT * FROM transDev;

-- ============================= LOAN_DEV VIEW =============================

DROP VIEW IF EXISTS loanDev_di_view;
CREATE VIEW loanDev_di_view AS
SELECT id, accountId, date, amount, duration, payments,
    CASE WHEN status = '-1'
    THEN 1
    ELSE 0
    END AS status
FROM loanDev;