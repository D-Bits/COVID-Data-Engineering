from unittest import TestCase
from requests import get


class TestEndpoints(TestCase):

    # Test that the endpoint for global data returns a 200
    def test_global_summary(self):

        endpoint = get("https://api.covid19api.com/summary").status_code
        self.assertEqual(endpoint, 200)

    def test_usa_history(self):

        endpoint = get("https://api.covidtracking.com/v1/us/daily.json").status_code
        self.assertEqual(endpoint, 200)

    def test_states_summary(self):

        endpoint = get("https://api.covidtracking.com/v1/states/current.json").status_code
        self.assertEqual(endpoint, 200)
    