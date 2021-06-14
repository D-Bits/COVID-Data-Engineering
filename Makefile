SHELL := /bin/bash


# Initialize project
init:
	python3 -m venv env
	source env/bin/activate; \
	pip3 install -r requirements.txt

# Bootstrap servers
start:
	sudo astro dev start -e .env

# Shutdown servers
stop:
	sudo astro dev stop

# Reset dev environment
kill:
	sudo astro dev kill

# Restart dev environment
restart:
	sudo astro dev stop
	sudo astro dev start

# Deploy to Astronomer Cloud
deploy:
	sudo astro dev deploy