/*
* Build necessary tables for the db
*/

CREATE DATABASE covid;

-- Create a new schema to contain tables for U.S. data
CREATE SCHEMA usa;

/*
* U.S. data table(s)
*/

-- Table for nationwide data history
CREATE TABLE usa.nation_history
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


-- Create a new schema to contain tables for U.S. data
CREATE SCHEMA world;

/*
* World data table(s)
*/
CREATE TABLE world.current_summary
(
    id SERIAL,
    country VARCHAR(255),
	
    PRIMARY KEY(id)
);
