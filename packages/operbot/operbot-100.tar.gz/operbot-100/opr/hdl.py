# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


"handler"


import queue
import threading
import time


from op.obj import Object
from opr.bus import Bus
from opr.cbs import Callbacks
from opr.thr import launch


def __dir__():
    return (
            "Handler",
           )


class Handler(Object):

    def __init__(self):
        Object.__init__(self)
        self.cache = Object()
        self.queue = queue.Queue()
        self.stopped = threading.Event()
        Bus.add(self)

    @staticmethod
    def forever():
        while 1:
            time.sleep(1.0)

    @staticmethod
    def handle(event):
        Callbacks.dispatch(event)

    def loop(self):
        while not self.stopped.isSet():
            self.handle(self.poll())

    def poll(self):
        return self.queue.get()

    def put(self, event):
        self.queue.put_nowait(event)

    @staticmethod
    def register(typ, cbs):
        Callbacks.add(typ, cbs)

    def restart(self):
        self.stop()
        self.start()

    def start(self):
        self.stopped.clear()
        launch(self.loop)

    def stop(self):
        self.stopped.set()
