.headers on
DROP VIEW IF EXISTS birth_decade_view;

CREATE VIEW birth_decade_view AS
    SELECT id, districtId, (substr(birthNumber, 1, 1) || '0') AS birth_decade from client;