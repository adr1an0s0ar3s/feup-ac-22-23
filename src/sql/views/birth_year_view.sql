.headers on
DROP VIEW IF EXISTS birth_year_view;

CREATE VIEW birth_year_view AS
    SELECT id, districtId, substr(birthNumber, 1, 2) AS birth_year from client;