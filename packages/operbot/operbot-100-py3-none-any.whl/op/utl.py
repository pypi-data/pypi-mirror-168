# This file is placed in the Public Domain.


"utility"


import os
import pathlib
import time


def __dir__():
    return (
            "cdir",
            "elapsed",
            "fns",
            "fntime",
            "fnclass",
            "spl"
           )


def cdir(path):
    "create directory allowing for saving of ``path``."
    if os.path.exists(path):
        return
    if os.sep in path:
        path = os.path.dirname(path)
    pathlib.Path(path).mkdir(parents=True, exist_ok=True)


def elapsed(seconds, short=True):
    "return string representing the elapsed time (``seconds`` is a diff)."
    txt = ""
    nsec = float(seconds)
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    sec = nsec - minutes*minute
    if years:
        txt += "%sy" % years
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += "%sd" % nrdays
    if years and short and txt:
        return txt
    if hours:
        txt += "%sh" % hours
    if nrdays and short and txt:
        return txt
    if minutes:
        txt += "%sm" % minutes
    if hours and short and txt:
        return txt
    if sec == 0:
        txt += "0s"
    else:
        txt += "%ss" % int(sec)
    txt = txt.strip()
    return txt


def fns(path, timed=None):
    "return all filenames matching, optionally within a time frame."
    if not path:
        return []
    if not os.path.exists(path):
        return []
    res = []
    for rootdir, dirs, _files in os.walk(path, topdown=False):
        for dname in  dirs:
            ddd = os.path.join(rootdir, dname)
            fls = sorted(os.listdir(ddd))
            if fls:
                opath = os.path.join(ddd, fls[-1])
                if (
                    timed
                    and "from" in timed
                    and timed["from"]
                    and fntime(opath) < timed["from"]
                   ):
                    continue
                if timed and timed.to and fntime(opath) > timed.to:
                    continue
                try:
                    fntime(opath)
                except ValueError:
                    continue
                opath = opath.split("store")[-1][1:]
                res.append(opath)
    return sorted(res, key=fntime)


def fntime(path):
    "return the time in a path."
    after = 0
    path = " ".join(path.split(os.sep)[-2:])
    if "." in path:
        path, after = path.rsplit(".")
    tme = time.mktime(time.strptime(path, "%Y-%m-%d %H:%M:%S"))
    if after:
        try:
            tme = tme + float(".%s"% after)
        except ValueError:
            pass
    return tme


def fnclass(path):
    "return type (class) in a path."
    try:
        _rest, *pth = path.split("Store")
    except ValueError:
        pth = path.split(os.sep)
    ppath = os.sep.join(pth)
    return ppath.split(os.sep)[0]


def spl(txt):
    "return list from comma seperated string."
    try:
        res = txt.split(",")
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]
