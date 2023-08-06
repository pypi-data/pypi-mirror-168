"""A package for handling an individual class."""


class Service:
    """A class for handling an individual service."""

    def __init__(self, name, status) -> None:
        """
        Create a Service object.

        Parameters
        ----------
        name : str
            The name of the service (e.g. S3).
        status : str
            The status of the service (e.g. available).
        """
        self.name = name
        self.status = status

    def is_available(self):
        """
        Check if the service is available/running.

        Returns
        -------
        bool
            True if the if the service is available or running,
            False otherwise.
        """
        if self.status in ['available', 'running']:
            return True

        return False
