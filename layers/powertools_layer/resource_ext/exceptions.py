class ResourceNotFoundError(Exception):  # -> Response 404
    """
    Exception raised when a specific resource is not found.

    This error is used to signify the absence of a required resource,
    which could be a file, database entry, or any other type of resource
    that is expected to be present but is not available or does not exist.

    """
