from munzee.endpoint import _Endpoint


class Map(_Endpoint):
    """Endpoint class for map."""

    endpoint = "map"

    def bounding_box(
        self,
        northeast: tuple,
        southwest: tuple,
        timestamp=0,
        limit=0,
        exclude="captured",
        fields="munzee_id,friendly_name,latitude,longitude,original_pin_image,proximity_radius_ft,creator_username",
    ):
        """
        Get deployed Munzees within a Bounding Box. Filter options can be applied.
        It’s possible to get more than one box at a time. Needed data fields can be specified.
        If the number of munzees in a box exceeds the maximum limit of 1000 munzees, returned data for that box will be picked randomly, so try to keep the boxes small.

        :param exclude: comma separated list of munzees status types that will be exluded. options: own, captured, maintenance
        :param fields: comma separated list of data fields for a munzee
        :param limit: maximum number of munzees to return. default: 1000
        :points: JSON encoded list of named bounding boxes to request.
        """
        return self.POST(
            "boundingbox",
            {
                "points": {
                    "box1": {
                        "timestamp": timestamp,
                        "lat1": northeast[0],
                        "lng1": northeast[1],
                        "lat2": southwest[0],
                        "lng2": southwest[1],
                    }
                },
                "exclude": exclude,
                "fields": fields,
                "limit": limit,
            },
        )
