# This file is placed in the Public Domain.
# pylint: disable=R0903


"selector"


from op.dft import Default


def __dir__():
    return (
            "Selector",
           )


class Selector(Default):

    "selector object."
