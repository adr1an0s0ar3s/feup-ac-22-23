SELECT A.accountId, A.balance
FROM transDev as A
LEFT OUTER JOIN transDev as B
    ON A.accountId = B.accountId AND A.date < B.date
WHERE B.accountId IS NULL
LIMIT(10);