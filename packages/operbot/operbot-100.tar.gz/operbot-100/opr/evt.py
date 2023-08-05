# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


import threading


from op.dft import Default
from op.obj import update
from opr.bus import Bus
from opr.prs import parse


def __dir__():
    return (
            "Event",
            "docmd"
           )


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready = threading.Event()
        self._result = []
        self.orig = repr(self)
        self.type = "event"

    def bot(self):
        return Bus.byorig(self.orig)

    def parse(self):
        if self.txt:
            update(self, parse(self.txt))

    def ready(self):
        self._ready.set()

    def reply(self, txt):
        self._result.append(txt)

    def show(self):
        for txt in self._result:
            Bus.say(self.orig, self.channel, txt)

    def wait(self):
        self._ready.wait()
        return self._result


def docmd(clt, txt):
    cmd = Event()
    cmd.channel = ""
    cmd.orig = repr(clt)
    cmd.txt = txt
    clt.handle(cmd)
    cmd.wait()
    return cmd
