"""
Munzee API wrapper.
"""
# import json

import json

import requests

from munzee.endpoints import Clans, Map, Munzees, Players, Statzee


class Munzee:
    """
    Munzee API wrapper.
    """

    def __init__(self, api_key):
        self._api_key = api_key
        self.base_url = "https://api.munzee.com/"

        """Setup the base_requester for the API."""
        self.base_requester = self.Requester(self._api_key)
        self.users = Players(self.base_requester)
        self.munzees = Munzees(self.base_requester)
        self.map = Map(self.base_requester)
        self.clans = Clans(self.base_requester)
        self.statzee = Statzee(self.base_requester)

    class Requester(object):
        """Api requesting object"""

        def __init__(self, api_key):
            self._api_key = api_key
            self.base_url = "https://api.munzee.com"

        def get_request(self, url):
            """
            Make a GET request to the API.
            """
            headers = {"Authorization": "Bearer " + self._api_key}
            response = requests.get(self.base_url + url, headers=headers)
            return response.json()

        def post_request(self, url, data):
            """
            Make a POST request to the API.
            """
            headers = {"Authorization": "Bearer " + self._api_key}
            files = {"data": (None, json.dumps(data))}
            response = requests.post(self.base_url + url, headers=headers, files=files)
            return response.json()
