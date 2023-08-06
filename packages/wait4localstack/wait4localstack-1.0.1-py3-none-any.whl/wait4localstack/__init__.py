"""
Wait for Localstack to be ready.

Localstack publishes which services it has been configured to execute and
their status (e.g. "running").  This module provides a class that will
check that the status of all services are "running".

Notes
-----
The service health checks for Localstack are described in detail in the
Localstack documentation see
https://github.com/localstack/localstack#service-health-checks

Examples
--------
To run with defaults simply have:

>>> from wait4localstack import Wait4Localstack
>>> wait4localstack = Wait4Localstack()
>>> wait4localstack.wait_for_all_services()
"""
import argparse
import logging
import sys
import time

import wait4localstack.localstack


class Wait4Localstack:
    """A class for waiting for Localstack to be ready."""

    def __init__(self, localstack_endpoint='http://localhost:4566/health',
                 maximum_retries=0, test_interval=2, exponential_backoff=False, log_level='WARN'):
        """
        Create a Wait4Localstack object.

        Parameters
        ----------
        localstack_endpoint : str,optional
            The url of the localstack endpoint to be checked (e.g. http://localhost:4566/health).  Default is
            http://localhost:4566/health
        maximum_retries : int,optional
            The max number of retries for attempting to check the endpoint.  If set to zero, will try for infinity.
            Default is zero.
        test_interval : int,optional
            The time in seconds between attempts.  Default is two.
        exponential_backoff : bool,optional
            If the number of seconds between attempts is to be doubled.  Default is False.
        log_level : str,optional
            What the log level should be for the utility.  Can be DEBUG, INFO or WARN.  Default is WARN.
        """
        self._exponential_backoff = None
        self._localstack_endpoint = None
        self._logger = None
        self._maximum_retries = None
        self._test_interval = None
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logger = logging.getLogger('wait4localstack')
        logger.setLevel(log_level)
        self.logger(logger)
        self.exponential_backoff(exponential_backoff)
        self.localstack_endpoint(localstack_endpoint)
        self.maximum_retries(maximum_retries)
        self.test_interval(test_interval)

    def exponential_backoff(self, exponential_backoff=None):
        """
        Get or set exponential backoff within the class.

        Parameters
        ----------
        exponential_backoff : bool,optional
            If provided, set if exponential backoff is True or False.

        Returns
        -------
        bool
            If exponential backoff is true or false.
        """
        logger = self.logger()

        if exponential_backoff is not None:
            logger.debug(f'Setting exponential backoff to {exponential_backoff}')
            self._exponential_backoff = exponential_backoff

        return self._exponential_backoff

    def localstack_endpoint(self, localstack_endpoint=None):
        """
        Get or set the localstack endpoint.

        Parameters
        ----------
        localstack_endpoint : str,optional
            The URL of the localstack endpoint (e.g. http://localstack:4566/health).

        Returns
        -------
        str
            The URL of the localstack endpoint.
        """
        logger = self.logger()

        if localstack_endpoint is not None:
            logger.debug(f'Setting localstack endpoint to {localstack_endpoint}')
            self._localstack_endpoint = localstack_endpoint

        return self._localstack_endpoint

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

    def maximum_retries(self, maximum_retries=None):
        """
        Get or set the maximum number of retries.

        Parameters
        ----------
        maximum_retries : int,optional
            The maximum number of retries.  If set to zero, then will try for infinity.

        Returns
        -------
        int
            The maximum number of retries.
        """
        logger = self.logger()

        if maximum_retries is not None:
            logger.debug(f'Setting maximum number of retries to {maximum_retries}')
            self._maximum_retries = maximum_retries

        return self._maximum_retries

    def test_interval(self, test_interval=None):
        """
        Get or set the interval between tests.

        If exponential backoff is enabled then this number will be doubled each time
        it is called.

        Parameters
        ----------
        test_interval : int,optional
            Set the interval between tests or if exponential backoff is enabled, set the initial wait period.

        Returns
        -------
        int
            The interval to the next test.
        """
        logger = self.logger()

        if test_interval is not None:
            logger.debug(f'Setting the test interval to {test_interval}')
            self._test_interval = test_interval

        response = self._test_interval

        if self.exponential_backoff():
            new_time_interval = self._test_interval * 2
            logger.debug(f'Setting new test level of {new_time_interval}')
            self._test_interval = new_time_interval
        else:
            logger.debug(f'Keeping test interval at {self._test_interval}')

        return response

    def wait_for_all_services(self):
        """Check the health endpoint until it is successful or max attempts has been reached."""
        logger = self.logger()
        connected = False
        attempts = 0
        max_retries = self.maximum_retries()

        while not connected:
            localstack = wait4localstack.localstack.LocalStack(self.localstack_endpoint(), logger)
            connected = localstack.is_live()

            if max_retries and attempts >= max_retries:
                logger.error(f'Localstack is not ready after {max_retries} attempts.')
                sys.exit(1)

            sleep_time = self.test_interval()

            if not connected:
                logger.debug(f'Will retry in {sleep_time} seconds.')
                attempts += 1
                time.sleep(sleep_time)


def command_line_interface(args):
    """
    Process arguments provided by the command line.

    Parameters
    ----------
    args : list of str
        The arguments to be processed.

    Returns
    -------
    args
        The command line arguments provided.
    """
    parser = argparse.ArgumentParser(args, description='Wait for Localstack to be ready.')
    parser.prog = 'wait4localstack'
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-d', '--debug', help='Should log level be DEBUG.', action='store_true')
    parser.add_argument('-e', '--endpoint',
                        help='The endpoint for the Localstack healthcheck (default http://localhost:4566/health).',
                        dest='localstack_endpoint', default='http://localhost:4566/health')
    help_str = 'The maximum retries.  If zero, try infinitely (default is zero).'
    parser.add_argument('-m', '--maximum-retries', help=help_str, type=int)
    help_str = 'The time in seconds to wait between retries (default is 2).'
    parser.add_argument('-t', '--test-interval', help=help_str, default=2, type=int)
    group.add_argument('-v', '--verbose', help='Should log level be INFO.', action='store_true')
    parser.add_argument('-x', '--exponential_backoff',
                        help='Should the time between retries by doubled at each attempt.',
                        dest='exponential_backoff', action='store_true')
    return parser.parse_args()


def main():
    """
    Provide an entry point for Wait4Localstack.

    This is the entrypoint for the executable script that then creates and
    consumes a Wait4Localstack object.
    """
    args = command_line_interface(sys.argv)

    if args.debug:
        log_level = 'DEBUG'
    elif args.verbose:
        log_level = 'INFO'
    else:
        log_level = 'WARN'

    widget = Wait4Localstack(args.localstack_endpoint,
                             args.maximum_retries,
                             args.test_interval,
                             args.exponential_backoff,
                             log_level)
    widget.wait_for_all_services()
