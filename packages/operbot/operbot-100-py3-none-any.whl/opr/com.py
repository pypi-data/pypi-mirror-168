# This file is placed in the Public Domain.
# pylint: disable=W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


from op.obj import Object


def __dir__():
    return (
            "Commands",
            "dispatch"
           )


class Commands(Object):

    cmds = {}

    @staticmethod
    def add(cmd):
        Commands.cmds[cmd.__name__] = cmd

    @staticmethod
    def get(cmd):
        return Commands.cmds.get(cmd)

    @staticmethod
    def remove(cmd):
        del Commands.cmds[cmd]


def dispatch(evt):
    evt.parse()
    func = Commands.get(evt.cmd)
    if func:
        func(evt)
        evt.show()
    evt.ready()
