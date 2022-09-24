PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS district;
CREATE TABLE district (
    id INT NOT NULL PRIMARY KEY,
    districtName TEXT NOT NULL,
    region TEXT NOT NULL,
    nInhabitants INT NOT NULL,
    nMunicipalitiesSub499Inhabitants INT NOT NULL,
    nMunicipalities500to1999Inhabitants INT NOT NULL,
    nMunicipalities2000to9999Inhabitants INT NOT NULL,
    nMunicipalitiesOver10000Inhabitants INT NOT NULL,
    nCities INT NOT NULL,
    urbanInhabitantsRatio REAL NOT NULL,
    averageSalary INT NOT NULL,
    unemploymentRate95 REAL NOT NULL,
    unemploymentRate96 REAL NOT NULL,
    nEnterpreneursPer1000Inhabitants INT NOT NULL,
    commitedCrimes95 INT NOT NULL,
    commitedCrimes96 INT NOT NULL
);

DROP TABLE IF EXISTS account;
CREATE TABLE account (
    id INT NOT NULL PRIMARY KEY,
    districtId INT NOT NULL REFERENCES district,
    frequency TEXT NOT NULL,
    date TEXT NOT NULL
);

DROP TABLE IF EXISTS client;
CREATE TABLE client (
    id INT NOT NULL PRIMARY KEY,
    birthNumber TEXT NOT NULL, -- "012345" is a valid number, using int would truncate the first 0
    districtId INT NOT NULL REFERENCES district
);

DROP TABLE IF EXISTS disp;
CREATE TABLE disp (
    id INT NOT NULL PRIMARY KEY,
    clientId INT NOT NULL REFERENCES client,
    accountId INT NOT NULL REFERENCES account,
    type TEXT NOT NULL
);

DROP TABLE IF EXISTS cardDev;
CREATE TABLE cardDev (
    id INT NOT NULL PRIMARY KEY,
    dispId INT NOT NULL REFERENCES disp,
    type TEXT NOT NULL,
    issued TEXT NOT NULL
);

DROP TABLE IF EXISTS loanDev;
CREATE TABLE loanDev (
    id INT NOT NULL PRIMARY KEY,
    accountId INT NOT NULL REFERENCES account,
    date TEXT NOT NULL,
    amount INT NOT NULL,
    duration INT NOT NULL,
    payments INT NOT NULL,
    status INT NOT NULL
);

DROP TABLE IF EXISTS permanentOrderDev;
CREATE TABLE permanentOrderDev (
    id INT NOT NULL PRIMARY KEY,
    accountId INT NOT NULL REFERENCES account,
    bankTo TEXT,
    accountTo INT NOT NULL REFERENCES account,
    amount INT NOT NULL,
    k_symbol TEXT
);

DROP TABLE IF EXISTS transDev;
CREATE TABLE transDev (
    id INT NOT NULL PRIMARY KEY,
    accountId INT NOT NULL REFERENCES account,
    date TEXT NOT NULL,
    type TEXT NOT NULL,
    operation TEXT,
    amount REAL NOT NULL,
    balance REAL NOT NULL,
    k_symbol TEXT,
    bank TEXT,
    account TEXT
);