# This file is placed in the Public Domain.
# pylint: disable=C0116


"utility"


import time


def __dir__():
    return (
            "wait",
           )


def wait():
    while 1:
        time.sleep(1.0)
