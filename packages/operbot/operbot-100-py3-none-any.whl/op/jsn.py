# This file is placed in the Public Domain.


"json"


import datetime
import json
import os


from json import JSONDecoder, JSONEncoder


from op.obj import Object, update
from op.utl import cdir
from op.wdr import Wd


def __dir__():
    return (
            'ObjectDecoder',
            'ObjectEncoder',
            'dump',
            'dumps',
            'load',
            'loads',
            'save'
           )


class ObjectDecoder(JSONDecoder):

    "object decoder (text to object)."

    def  __init__(self, *args, **kwargs):
        "decoder constructor"
        JSONDecoder.__init__(self, *args, **kwargs)

    def decode(self, s, _w=None):
        "decode string ``s`` into an Object."
        value = json.loads(s)
        return Object(value)

    def raw_decode(self, s, *args, **kwargs):
        "return object and index into the string at it's end."
        return JSONDecoder.raw_decode(self, s, *args, **kwargs)


class ObjectEncoder(JSONEncoder):

    "object encoder (object to text)."

    def  __init__(self, *args, **kwargs):
        "encoder constructor"
        JSONEncoder.__init__(self, *args, **kwargs)

    def encode(self, o):
        "encode object ``o`` to a json string."
        return JSONEncoder.encode(self, o)

    def default(self, o):
        "return string representation object ``o``."
        if isinstance(o, dict):
            return o.items()
        if isinstance(o, Object):
            return vars(o)
        if isinstance(o, list):
            return iter(o)
        if isinstance(o,
                      (type(str), type(True), type(False),
                       type(int), type(float))
                     ):
            return o
        try:
            return JSONEncoder.default(self, o)
        except TypeError:
            return str(o)

    def iterencode(self, o, *args, **kwargs):
        "return strings while parsing object ``o``."
        return JSONEncoder.iterencode(self, o, *args, **kwargs)


def dump(obj, opath):
    "save object to file with path ``opath``."
    cdir(opath)
    with open(opath, "w", encoding="utf-8") as ofile:
        json.dump(
            obj.__dict__, ofile, cls=ObjectEncoder, indent=4, sort_keys=True
        )
    return obj.__stp__


def dumps(obj):
    "return json string representation."
    return json.dumps(obj, cls=ObjectEncoder)


def hook(path):
    "reconstruct object from json file ."
    #splitted = hfn.split(os.sep)
    #cname = fnclass(hfn)
    #cls = Class.get(cname)
    obj = Object()
    load(obj, path)
    return obj


def load(obj, opath):
    "load object from path ``opath``."
    splitted = opath.split(os.sep)
    stp = os.sep.join(splitted[-4:])
    lpath = os.path.join(Wd.workdir, "store", stp)
    if os.path.exists(lpath):
        with open(lpath, "r", encoding="utf-8") as ofile:
            res = json.load(ofile, cls=ObjectDecoder)
            update(obj, res)
    obj.__stp__ = stp


def loads(jss):
    "create object from json string."
    return json.loads(jss, cls=ObjectDecoder)


def save(obj):
    "save the object."
    prv = os.sep.join(obj.__stp__.split(os.sep)[:1])
    obj.__stp__ = os.path.join(
                       prv,
                       os.sep.join(str(datetime.datetime.now()).split())
                      )
    opath = Wd.getpath(obj.__stp__)
    dump(obj, opath)
    os.chmod(opath, 0o444)
    return obj.__stp__
