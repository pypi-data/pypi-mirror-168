"""Models for Open Data Platform of Zurich."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class DisabledParking:
    """Object representing a disabled parking."""

    spot_id: int
    address: str

    longitude: float
    latitude: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DisabledParking:
        """Return a DisabledParking object from a dictionary.

        Args:
            data: The data from the API.

        Returns:
            A DisabledParking object.
        """

        attr = data["properties"]
        geo = data["geometry"]["coordinates"]
        return cls(
            spot_id=int(attr.get("objectid")),
            address=attr.get("adresse"),
            longitude=geo[0],
            latitude=geo[1],
        )
