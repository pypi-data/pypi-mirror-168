class _Endpoint(object):
    """
    Base class for all endpoints.
    """

    def __init__(self, requester):
        self._requester = requester

    def _expanded_path(self, path=None) -> str:
        """Gets the expanded path, given this endpoint"""
        return "/{expanded_path}".format(
            expanded_path="/".join(p for p in (self.endpoint, path) if p)
        )

    def GET(self, url) -> dict:
        """
        Make a GET request to the API.
        """
        return self._requester.get_request(self._expanded_path(url))

    def POST(self, url, data) -> dict:
        """
        Make a POST request to the API.
        """
        return self._requester.post_request(self._expanded_path(url), data)
