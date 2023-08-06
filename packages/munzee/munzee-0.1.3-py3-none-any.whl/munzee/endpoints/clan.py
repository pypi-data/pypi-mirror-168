from munzee.endpoint import _Endpoint


class Clans(_Endpoint):
    """Endpoint class for clans."""

    endpoint = "clan"

    def get_clan_id(self, name: str):
        """
        Convert a clan’s simple name into the correcponsing clan ID needed for other requests.
        """
        return self.POST("id", {"simple_name": name})

    def get_clan_details(self, clan_id: int):
        """
        Get details for a specific clan and all clan members. Point values are for the current clan battle.
        """
        return self.POST("", {"clan_id": clan_id})

    def get_clan_statistics(self, clan_id: int):
        """
        Get current statistics for a specific clan.

        Data can be null if there is no data or no clan battle running currently.
        """
        return self.POST("stats", {"clan_id": clan_id})
