.headers on

DROP VIEW IF EXISTS shared_account_view;

CREATE VIEW shared_account_view
AS
SELECT accountId, COUNT(*) > 1 AS is_shared 
FROM disp 
GROUP BY accountId;