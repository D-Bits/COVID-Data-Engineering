/*
* Build necessary tables for the db
*/



/*
* U.S. data table(s)
*/

DROP TABLE IF EXISTS usa.nation_history;

-- Table for nationwide data history
CREATE TABLE IF NOT EXISTS usa.nation_history
(
	id SERIAL,
	"dateChecked" TIMESTAMP,
	positive INT, 
	death INT,
	"deathIncrease" INT,
	recovered INT,
	hospitalized INT,
	"hospitalizedIncrease" INT,
	"hospitalizedCumulative" INT, 
	"onVentilatorCurrently" INT,
	"onVentilatorCumulative" INT,
	PRIMARY KEY(id)
);


/*
* World data table(s)
*/
CREATE TABLE IF NOT EXISTS world.global_summary
(
    id SERIAL,
    "Country" VARCHAR(255) NOT NULL,
	"NewConfirmed" INT NOT NULL,
    "TotalConfirmed" INT NOT NULL,
    "NewDeaths" INT NOT NULL,
    "TotalDeaths" INT NOT NULL,
    "NewRecovered" INT NOT NULL,
    "TotalRecovered" INT NOT NULL,
    "Date" TIMESTAMP,
	"CountryCode" VARCHAR(2),
    PRIMARY KEY(id)
);
