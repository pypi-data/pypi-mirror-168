# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


from op.obj import Object


def __dir__():
    return (
            "Callbacks",
           )


class Callbacks(Object):

    cbs = {}

    @staticmethod
    def add(typ, cbs):
        if typ not in Callbacks.cbs:
            Callbacks.cbs[typ] = cbs

    @staticmethod
    def callback(event):
        func = Callbacks.cbs.get(event.type)
        if not func:
            event.ready()
            return
        func(event)

    @staticmethod
    def dispatch(event):
        Callbacks.callback(event)

    @staticmethod
    def get(typ):
        return Callbacks.cbs.get(typ)
