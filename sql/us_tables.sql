/*
* Build necessary tables for the db
*/

-- Create a new schema to contain tables for covid data
CREATE SCHEMA usa;

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

-- State COVID data history
CREATE TABLE usa.state_history
(
	id SERIAL,
	state_name VARCHAR(255) NOT NULL,
	
);
