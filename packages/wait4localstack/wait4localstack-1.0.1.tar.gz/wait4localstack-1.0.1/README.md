# wait4localstack
A Python package for ensuring that localstack has fully started.

## Application Programming Interface (API) Documentation

To see the documentation for the API (auto-generated) please see
https://github.com/locp/wait4localstack/blob/main/docs/index.md

## Command Line Interface (CLI) Interface

A script called `wait4localstack` is provided the synopsis of the
command is:

```
usage: wait4localstack [-h] [-d] [-e LOCALSTACK_ENDPOINT] [-m MAXIMUM_RETRIES] [-t TEST_INTERVAL] [-v] [-x]

Wait for Localstack to be ready.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           Should log level be DEBUG.
  -e LOCALSTACK_ENDPOINT, --endpoint LOCALSTACK_ENDPOINT
                        The endpoint for the Localstack healthcheck (default http://localhost:4566/health).
  -m MAXIMUM_RETRIES, --maximum-retries MAXIMUM_RETRIES
                        The maximum retries. If zero, try infinitely (default is zero).
  -t TEST_INTERVAL, --test-interval TEST_INTERVAL
                        The time in seconds to wait between retries (default is 2).
  -v, --verbose         Should log level be INFO.
  -x, --exponential_backoff
                        Should the time between retries by doubled at each attempt.
```


