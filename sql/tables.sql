/*
* Build necessary tables for the db
*/

-- Create a new schema to contain tables for covid data
CREATE SCHEMA covid;

-- Table for nationwide data history
CREATE TABLE covid.nation_history
(
	id SERIAL,
	recorded_date INT,
	cases INT NOT NULL, 
	deaths INT NOT NULL,
	new_deaths INT NOT NULL,
	deaths_increase INT NOT NULL,
	hospitalized_currently INT NOT NULL,
	hospitalized_cumulatively INT NOT NULL,
	hospitalization_increase INT NOT NULL,
	ventilator_currently INT NOT NULL,
	ventilator_cumulatively INT NOT NULL,
	PRIMARY KEY(id)
);

-- State COVID data history
CREATE TABLE covid.state_history
(
	id SERIAL,
	state_name VARCHAR(255) NOT NULL,
	
);
