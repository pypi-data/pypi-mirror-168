from munzee.endpoint import _Endpoint


class Munzees(_Endpoint):
    """Endpoint class for munzees."""

    endpoint = "munzee"

    def get_munzee_by_id(self, id: int, closest=0):
        """
        Get a Munzee by ID.
        """
        return self.POST("", {"munzee_id": id, "closest": closest})

    def get_munzee_by_url(self, url: str, closest=0):
        """
        Get a Munzee by URL.
        """
        return self.POST("", {"url": url, "closest": closest})

    def get_latest_logs(self, munzee_id: int):
        """
        Get the latest logs for a Munzee.
        """
        return self.POST("logs", {"munzee_id": munzee_id})

    def has_user_captured_munzee(self, munzee_id: int):
        """
        Check if a user has captured a Munzee.
        """
        return self.POST("hascaptured", {"munzee_ids": munzee_id})
