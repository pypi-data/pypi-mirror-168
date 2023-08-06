"""Asynchronous Python client providing Open Data information of Zurich."""


class ODPZurichError(Exception):
    """Generic Open Data Platform Zurich exception."""


class ODPZurichConnectionError(ODPZurichError):
    """Open Data Platform Zurich - connection error."""
