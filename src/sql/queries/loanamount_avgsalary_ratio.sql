SELECT loanDev.id as loanId, accountId, date, amount as loanAmount, averageSalary, (amount*1.0 / averageSalary) as ratio, duration, status
    FROM loanDev
    JOIN (
        SELECT averageSalary, account.id
        FROM account
        JOIN district
            WHERE account.districtId = district.id
    ) AS account
    WHERE loanDev.accountId = account.id
;