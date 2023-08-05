# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903



from opr.com import dispatch
from opr.hdl import Handler


def __dir__():
    return (
            "Client",
           )


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.ignore = []
        self.orig = repr(self)
        self.register("event", dispatch)

    def announce(self, txt):
        self.raw(txt)

    def raw(self, txt):
        raise NotImplementedError("raw")

    def say(self, channel, txt):
        if channel not in self.ignore:
            self.raw(txt)
