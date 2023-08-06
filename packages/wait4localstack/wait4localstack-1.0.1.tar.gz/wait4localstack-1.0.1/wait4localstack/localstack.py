"""A package for monitoring the status of a LocalStack service."""
import json
from unicodedata import name
import urllib3

import wait4localstack.service


class LocalStack:
    """A class for monitoring the status of a LocalStack service."""

    def __init__(self, connection_url, logger) -> None:
        """
        Create a LocalStack object.

        Parameters
        ----------
        connection_url : str
            The URL to connect to.
        logging.Logger
            The logger to use for logging.
        """
        self.connection_url = connection_url
        self.logger(logger)
        self.service_names = []
        self.services = {}
        data = self.get_connection_details()
        self.parse_services(data)

    def get_connection_details(self):
        """
        Poll the connection endpoint until we get a parsable status.

        Returns
        -------
        dict
            The connection string having being parsed as JSON.
        """
        data = {}
        logger = self.logger()
        http = urllib3.PoolManager()

        try:
            logger.debug(f'Making HTTP request to {self.connection_url}')
            r = http.request('GET', self.connection_url)

            if r.status == 200:
                logger.debug(f'Response is "{r.data}".')
                data = json.loads(r.data)
                logger.debug(f'Data is "{data}".')
            else:
                logger.warning(f'Unexpected status ({r.status}) from {self.connection_url}.')
        except urllib3.exceptions.MaxRetryError as e:
            logger.warning(f'Unable to connect to {self.connection_url} "{e.reason}".')

        return data

    def is_live(self):
        """
        Check if all services are available.

        Returns
        -------
        bool
            True if all services are available, False otherwise.
        """
        live_services_count = 0
        services_count = len(self.service_names)
        logger = self.logger()

        for service_name in self.service_names:
            service = self.services[service_name]

            if service.is_available():
                logger.info(f'Service {service_name} is available/running.')
                live_services_count += 1
            else:
                logger.error(f'Service {service_name} status is {service.status}.')

        return (services_count and live_services_count == services_count)

    def logger(self, logger=None):
        """
        Get or set the logger.

        Parameters
        ----------
        logger : logging.Logger
            The logger to use for logging.

        Returns
        -------
        logging.Logger
            The logger to use for logging.
        """
        if logger is not None:
            self._logger = logger
        return self._logger

    def parse_services(self, data):
        """
        Parse the health information as returned by the LocalStack health endpoint.

        Parameters
        ----------
        data : dict
            The data (parsed from JSON text).
        """
        logger = self.logger()
        self.service_names = []
        self.services = {}

        try:
            services = data['services']

            for service_name in services:
                service_status = services[service_name]
                logger.debug(f'Status of {service_name} is {service_status}.')
                service = wait4localstack.service.Service(name, service_status)
                self.service_names.append(service_name)
                self.services[service_name] = service
        except KeyError:
            logger.error(f'Unable to parse health endpoint response ("{json.dumps(data)}").')
