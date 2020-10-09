"""
Script to setup project/dev environment, and fix certain Docker problems.
"""
from subprocess import run, CalledProcessError


# Clean things (including volumes) up before building
run(['docker', 'system', 'prune']).check_returncode()
run(['docker', 'volume', 'rm', 'covid-data_covid']).check_returncode()
run(['docker-compose', 'build']).check_returncode()
run(['docker-compose', 'up']).check_returncode()

