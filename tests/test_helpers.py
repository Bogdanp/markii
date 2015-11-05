import bootstrap  # noqa
import inspect


def test_getrusage():
    from markii.markii import getrusage

    try:
        import resource  # noqa
        assert getrusage()
    except ImportError:
        assert getrusage() is None


def test_getsource():
    from markii.markii import getsource

    def f():
        return 42

    assert getsource(f) == """\
def f():
    return 42
"""


def test_getprocinfo_no_resource():
    from markii.markii import getprocinfo

    assert getprocinfo()

    module = inspect.getmodule(getprocinfo)
    old_resource = module.resource
    module.resource = None
    assert getprocinfo() is None
    module.resource = old_resource


def test_getsource_builtin():
    from markii.markii import getsource
    assert getsource(list) == ""


def test_getprocinfo():
    from markii.markii import resource, getprocinfo

    process = getprocinfo()
    if not resource:
        assert process is None

    assert "utime" in process
    assert "stime" in process
    assert "mem" in process

    assert isinstance(process.get("utime"), basestring)
    assert isinstance(process.get("stime"), basestring)
    assert isinstance(process.get("mem"), basestring)


def test_deident():
    from markii.markii import deindent
    source = """\
    def foo():
        return 42
"""
    target = """\
def foo():
    return 42
"""
    assert deindent(source) == target


def test_deident_unindented():
    from markii.markii import deindent
    source = """\
def foo():
    return 42
"""
    assert deindent(source) == source


def test_getframes():
    from markii.markii import getframes

    def f():
        raise Exception()

    def g():
        return f()

    def h():
        return g()

    try:
        h()
    except:
        frames = getframes()
        assert frames
        assert len(frames) == 4
        assert frames[0].func == "f"
        assert frames[1].func == "g"
        assert frames[2].func == "h"
        assert frames[3].func == "test_getframes"


def test_getframes_class_instance():
    from markii.markii import getframes

    class Foo(object):
        @classmethod
        def fm(cls):
            raise Exception()

        def gm(self):
            return self.fm()

        def f(self):
            raise Exception()

        def g(self):
            return self.f()

    try:
        Foo().g()
    except:
        frames = getframes()
        assert frames
        assert len(frames) == 3
        assert frames[0].func == "f"
        assert frames[1].func == "g"
        assert frames[2].func == "test_getframes_class_instance"

    try:
        Foo().gm()
    except:
        frames = getframes()
        assert frames
        assert len(frames) == 3
        assert frames[0].func == "fm"
        assert frames[1].func == "gm"
        assert frames[2].func == "test_getframes_class_instance"


def test_getframes_class_instance_gcd():
    from markii.markii import getframes

    class Foo(object):
        def f(self):
            self = None  # noqa
            raise Exception()

        def g(self):
            return self.f()

    try:
        Foo().g()
    except:
        frames = getframes()
        assert frames
        assert len(frames) == 3
        assert frames[0].func == "f"
        assert frames[1].func == "g"
        assert frames[2].func == "test_getframes_class_instance_gcd"


def test_rendering():
    from markii import markii

    def f(self):
        raise Exception()

    try:
        f()
    except Exception as e:
        assert markii(e)
