import json

from typing_extensions import TypedDict
from pydantic import BaseModel

from munzee.endpoint import _Endpoint


class _Capture(BaseModel):
    capture_id: int
    captured_at: str
    points: int
    code: int
    friendly_name: str
    capture_type_id: int
    munzee_id: int
    username: str
    pin: str


class _CapOn(_Capture):
    points_for_creator: int
    deployed_at: str
    latitude: float


class _Deploy(BaseModel):
    id: int
    deployed_at: str
    points: int
    code: int
    friendly_name: str
    capture_type_id: int
    pin: str


class _Data(BaseModel):
    captures: list[_Capture]
    captures_on: list[_CapOn]
    deploys: list[_Deploy]
    # todo - add passives, and archives


class Response(TypedDict):
    status_code: int


class PydanticResponse(BaseModel):
    status_code: int
    data: _Data


class Statzee(_Endpoint):
    """Endpoint class for statzee."""

    endpoint = "statzee"

    def get_daily_stats(self, day: str) -> PydanticResponse:
        """
        Get the user's daily stats.
        """

        response = PydanticResponse.parse_obj(self.POST("player/day", {"day": day}))
        return response
