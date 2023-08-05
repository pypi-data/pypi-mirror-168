# This file is placed in the Public Domain.
# pylint: disable=W0613


"object"


import datetime
import os
import types


from op.cls import Class


def __dir__():
    return (
            'Class',
            'Default',
            'Object',
            'Wd',
            'delete',
            'edit',
            'get',
            'items',
            'jsn',
            'keys',
            'name',
            'otype',
            'printable',
            'register',
            'save',
            'types',
            'update',
            'values'
           )


class Object:

    "big object."

    __slots__ = ('__dict__','__stp__')

    def __init__(self, *args, **kwargs):
        object.__init__(self)
        self.__stp__ = os.path.join(
            otype(self),
            os.sep.join(str(datetime.datetime.now()).split()),
        )
        if args:
            try:
                self.__dict__.update(vars(args[0]))
            except TypeError:
                self.__dict__.update(args[0])

    def __iter__(self):
        return iter(self.__dict__)

    def __len__(self):
        return len(self.__dict__)

    def __repr__(self):
        return repr(self.__dict__)

    def __str__(self):
        return str(self. __dict__)


Class.add(Object)


def delete(obj, key):
    "delete attribute ``key``."
    delattr(obj, key)


def edit(obj, setter):
    "set items with values in a setter (key/value dict)."
    for key, value in items(setter):
        register(obj, key, value)


def printable(obj, args="", skip="", plain=False):
    "return printable string."
    res = []
    keyz = []
    if "," in args:
        keyz = args.split(",")
    if not keyz:
        keyz = keys(obj)
    for key in keyz:
        if key.startswith("_"):
            continue
        if skip:
            skips = skip.split(",")
            if key in skips:
                continue
        value = getattr(obj, key, None)
        if not value:
            continue
        if " object at " in str(value):
            continue
        txt = ""
        if plain:
            txt = str(value)
        elif isinstance(value, str) and len(value.split()) >= 2:
            txt = '%s="%s"' % (key, value)
        else:
            txt = '%s=%s' % (key, value)
        res.append(txt)
    txt = " ".join(res)
    return txt.rstrip()


def get(obj, key, default=None):
    "return item ``key``."
    return obj.__dict__.get(key, default)


def name(obj):
    "return full qualified name."
    typ = type(obj)
    if isinstance(typ, types.ModuleType):
        return obj.__name__
    if "__self__" in dir(obj):
        return "%s.%s" % (obj.__self__.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj) and "__name__" in dir(obj):
        return "%s.%s" % (obj.__class__.__name__, obj.__name__)
    if "__class__" in dir(obj):
        return obj.__class__.__name__
    if "__name__" in dir(obj):
        return obj.__name__
    return None


def items(obj):
    "return key/value pairs of the object ``obj``."
    if isinstance(obj, type({})):
        return obj.items()
    return obj.__dict__.items()


def keys(obj):
    "return keys of object ``obj``."
    return obj.__dict__.keys()


def otype(obj):
    "return object type of object ``obj``."
    return str(type(obj)).split()[-1][1:-2]


def register(obj, key, value):
    "register key/value on object ``obj``."
    setattr(obj, key, value)


def update(obj, data):
    "update object ``obj`` with a key/value dict."
    for key, value in items(data):
        setattr(obj, key, value)

def values(obj):
    "return values of object ``obj``."
    return obj.__dict__.values()
