# -*- coding: utf-8 -*-
"""
General utility functions and classes.
"""

import datetime
from timeit import default_timer


class Timer(object):
    """
    A context manager to help measure execution times.

    Example
    ---
    ```
    with Timer() as t:
        # do something interesting
    print(t.delta)  # X days, X:XX:XX
    ```
    """

    def __init__(self):
        self.timer = default_timer

    def __enter__(self):
        self.start = self.timer()
        return self

    def __exit__(self, *args):
        end = self.timer()
        self.elapsed = end - self.start
        self.delta = datetime.timedelta(seconds=self.elapsed)
