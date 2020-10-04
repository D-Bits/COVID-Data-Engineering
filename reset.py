"""
Script to setup project/dev environment, and fix certain Docker problems.
"""
from subprocess import run, CalledProcessError


try:
    # Clean things (including volumes) up before building
    run(['docker', 'system', 'prune']).check_returncode()
    run(['docker', 'volume', 'rm', 'us-covid-data_uscovid']).check_returncode()
    run(['docker-compose', 'build']).check_returncode()
    run(['docker-compose', 'up']).check_returncode()
    
except CalledProcessError:
    print("ERROR: A command failed to execute. We apologize for the inconvience.")
