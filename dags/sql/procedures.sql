CREATE OR REPLACE PROCEDURE sp_update_states_data
(
	present_date INT,
	present_cases INT, 
	present_deaths INT,
	present_new_deaths INT,
	present_recovered INT, 
	present_hospitalized_currently INT,
	present_hospitalized_cumulatively INT,
	present_ventilator_currently INT,
	present_ventilator_cumulatively INT
)

LANGUAGE SQL

AS $$

INSERT INTO covid.nation_history 
(
	recorded_date,
	cases, 
	deaths,
	new_deaths,
	recovered,
	hospitalized_currently,
	hospitalized_cumulatively,
	ventilator_currently,
	ventilator_cumulatively
)
VALUES 
(
	present_date,
	present_cases, 
	present_deaths,
	present_new_deaths,
	present_recovered,
	present_hospitalized_currently,
	present_hospitalized_cumulatively,
	present_ventilator_currently,
	present_ventilator_cumulatively
);

$$;