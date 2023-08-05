# This file is placed in the Public Domain.


"path tests"


import unittest


from op.utl import fntime


FN = "store/opr.evt.Event/2022-04-11/22:40:31.259218"


class TestPath(unittest.TestCase):

    "path tests."

    def test_path(self):
        "check fntime."
        fnt = fntime(FN)
        self.assertEqual(fnt, 1649709631.259218)
