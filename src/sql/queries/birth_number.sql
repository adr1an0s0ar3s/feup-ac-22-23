SELECT id,
    CASE WHEN substr(birthNumber,3,2) > '50'
    THEN substr(birthNumber,1,2) || substr('0' || (substr(birthNumber,3,2)-50),-2,2) || substr(birthNumber,5,2)
    ELSE birthNumber
    END AS birthNumber
FROM client
LIMIT(10);