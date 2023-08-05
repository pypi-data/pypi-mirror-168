# This file is placed in the Public Domain.


"classes"


def __dir__():
    return (
            "Class",
           )


class Class:

    "classes to use in path names."

    cls = {}

    @staticmethod
    def add(clz):
        "add a class."
        Class.cls["%s.%s" % (clz.__module__, clz.__name__)] =  clz

    @staticmethod
    def all():
        "return all registered classes."
        return Class.cls.keys()

    @staticmethod
    def full(name):
        "match full names."
        name = name.lower()
        res = []
        for cln in Class.cls:
            if name == cln.split(".")[-1].lower():
                res.append(cln)
        return res

    @staticmethod
    def get(name):
        "return specific class."
        return Class.cls.get(name, None)

    @staticmethod
    def remove(name):
        "remove a registered class."
        del Class.cls[name]
