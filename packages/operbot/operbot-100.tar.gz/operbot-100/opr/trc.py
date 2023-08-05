# This file is placed in the Public Domain.
# pylint: disable=C0114,C0115,C0116,R0903


import os
import traceback


from op.obj import name


def from_exception(exc):
    result = []
    for frm in traceback.extract_tb(exc.__traceback__)[::-1]:
        result.append("%s:%s" % (os.sep.join(frm.filename.split(os.sep)[-2:]), frm.lineno))
    return "%s(%s) %s" % (name(exc), exc, " ".join(result))
