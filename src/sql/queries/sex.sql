SELECT id,
    CASE WHEN substr(birthNumber,3,2) > "50"
    THEN "female"
    ELSE "male"
    END AS sex
FROM client
LIMIT(10);