class CausarException(Exception):
    """Base module exception."""


class CacheLookupFailed(CausarException):
    """Failed to find the provided item in the cache.

    Did you add it?
    """
