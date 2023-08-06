from munzee.endpoint import _Endpoint


class Players(_Endpoint):
    """Endpoint class for players."""

    endpoint = "user"

    def get_current_player(self):
        """
        Get the user's profile.
        """
        return self.GET("current")

    def get_player_by_name(self, name: str):
        """
        Get a player by their name.
        """
        return self.POST("", {"username": name})

    def get_player_by_id(self, user_id: int):
        """
        Get a player by their ID.
        """
        return self.POST("", {"user_id": user_id})
