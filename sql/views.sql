/*
* Views for analyizing world data.
*/


-- Show countries w/ worst cases of COVID-19
CREATE VIEW world.top_cases AS
(
    SELECT "Country", "TotalConfirmed", "NewConfirmed"
    FROM world.global_summary
    ORDER BY "TotalConfirmed" DESC
);


-- Show countries w/ worst death tolls of COVID-19
CREATE VIEW world.top_deaths AS
(
	SELECT "Country", "TotalDeaths", "NewDeaths"
	FROM world.global_summary 
	ORDER BY "TotalDeaths" DESC 
);

