"""Example of metrics decorator"""

from functools import wraps
from time import monotonic
from sys import exc_info
import logging


logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)


class MetricsClient:
    def __init__(self, url):
        # TODO: Create system client here
        self.url = url

    def __call__(self, fn):
        @wraps(fn)
        def wrapper(*args, **kw):
            start = monotonic()
            error = None
            try:
                return fn(*args, **kw)
            finally:
                duration = monotonic() - start
                # TODO: send metric to server
                logging.info('%s took %.3fsec', fn.__name__, duration)
                _, error, _ = exc_info()
                if error is not None:
                    logging.error('%s error: %s', fn.__name__, error)

        return wrapper

    def __repr__(self):
        name = self.__class__.__name__
        return f'{name}({self.url!r})'


# Example usage
if __name__ == '__main__':
    from time import sleep

    metrics = MetricsClient('http://localhost:8000')

    @metrics
    def query(expr):
        """Run a query on our database"""
        if not expr:
            raise ValueError('empty query')

        sleep(0.3)  # Simulate work
        return [('car1', 3.2), ('car2', 1.2), ('car1', 4.1)]

    query('SELECT card_id, distance FROM rides')
    try:
        query('')
    except ValueError:
        pass
