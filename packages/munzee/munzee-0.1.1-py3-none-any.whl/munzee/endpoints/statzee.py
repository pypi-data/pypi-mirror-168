from munzee.endpoint import _Endpoint


class Statzee(_Endpoint):
    """Endpoint class for statzee."""

    endpoint = "statzee"

    def get_daily_stats(self, day: str):
        """
        Get the user's daily stats.
        """
        return self.POST("player/day", {"day": day})
