# This file is placed in the Public Domain.
# pylint: disable=W0611,W0622,E1101,W0613,W0221,W0201,C0112,C0103,C0114,C0115,C0116,R0902,R0903


"command"


import threading
import time


from op.cls import Class
from op.dbs import find, fntime
from op.obj import Object, get, name, printable, update
from op.jsn import save
from op.utl import elapsed
from opr.bus import Bus
from opr.com import Commands
from oper.run import starttime


def __dir__():
    return (
            "cmd",
            "dne",
            "flt",
            "log",
            "sts",
            "thr",
            "todo",
            "upt"
           )


class Log(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


class Todo(Object):

    def __init__(self):
        super().__init__()
        self.txt = ""


def cmd(event):
    event.reply(",".join(sorted(Commands.cmds)))


def dne(event):
    if not event.args:
        return
    selector = {"txt": event.args[0]}
    for _fn, obj in find("todo", selector):
        obj.__deleted__ = True
        save(obj)
        event.reply("ok")
        break


def flt(event):
    try:
        index = int(event.args[0])
        event.reply(Bus.objs[index])
        return
    except (KeyError, TypeError, IndexError, ValueError):
        pass
    event.reply(" | ".join([name(o) for o in Bus.objs]))


def log(event):
    if not event.rest:
        _nr = 0
        for _fn, obj in find("log"):
            event.reply("%s %s %s" % (
                                      _nr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(_fn)))
                                     )
            _nr += 1
        return
    obj = Log()
    obj.txt = event.rest
    save(obj)
    event.reply("ok")


def sts(event):
    for bot in Bus.objs:
        try:
            event.reply("%s: %s (%s)" % (
                                         bot.cfg.server,
                                         format(bot.state, skip="last"),
                                         elapsed(time.time()-bot.state.last))
                                        )
        except AttributeError:
            continue


def tdo(event):
    if not event.rest:
        nmr = 0
        for _fn, obj in find("todo"):
            event.reply("%s %s %s" % (
                                      nmr,
                                      obj.txt,
                                      elapsed(time.time() - fntime(_fn)))
                                     )
            nmr += 1
        return
    obj = Todo()
    obj.txt = event.rest
    save(obj)
    event.reply("ok")


def thr(event):
    result = []
    for thread in sorted(threading.enumerate(), key=lambda x: x.getName()):
        if str(thread).startswith("<_"):
            continue
        obj = Object()
        update(obj, vars(thread))
        if get(obj, "sleep", None):
            uptime = obj.sleep - int(time.time() - obj.state.latest)
        else:
            uptime = int(time.time() - obj.starttime)
        result.append((uptime, thread.getName()))
    res = []
    for uptime, txt in sorted(result, key=lambda x: x[0]):
        res.append("%s/%s" % (txt, elapsed(uptime)))
    if res:
        event.reply(" ".join(res))
    else:
        event.reply("no threads running")


def upt(event):
    event.reply(elapsed(time.time()-starttime))
