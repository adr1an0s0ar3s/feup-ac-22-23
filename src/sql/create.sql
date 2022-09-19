DROP TABLE IF EXISTS account;
CREATE TABLE account (
    id INT NOT NULL PRIMARY KEY,
    districtId INT NOT NULL,
    frequency TEXT NOT NULL,
    date INT NOT NULL
);

DROP TABLE IF EXISTS client;
CREATE TABLE client (
    id INT NOT NULL PRIMARY KEY,
    birthNumber TEXT NOT NULL, -- "012345" is a valid number, using int would truncate the first 0
    districtId INT NOT NULL
)