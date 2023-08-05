# This file is placed in the Public Domain.


from setuptools import setup


def read():
    return open("README.rst", "r").read()


setup(
    name="operbot",
    version="100",
    author="Bart Thate",
    author_email="operbot100@gmail.com",
    url="http://github.com/operbot/operbot",
    description="write your own commands",
    long_description=read(),
    license="Public Domain",
    packages=["op", "opr", "oper"],
    scripts=["bin/op", "bin/operbot"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: Public Domain",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Intended Audience :: System Administrators",
        "Topic :: Communications :: Chat :: Internet Relay Chat",
        "Topic :: Software Development :: Libraries :: Python Modules",
     ],
)
