import sys

from markii.appengine import fix_appengine


def test_workaround():
    del sys.modules["__main__"]
    fix_appengine()
    assert sys.modules["__main__"]
    assert sys.modules["__main__"].sys
