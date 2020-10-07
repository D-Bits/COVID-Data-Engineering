/*
* Views for analyizing world data.
*/


-- Show data for all countries with cases descendind
CREATE VIEW top_cases AS
(
    SELECT "Country", "TotalConfirmed", "NewConfirmed"
    FROM global_summary
    ORDER BY "TotalConfrimed" DESC
);