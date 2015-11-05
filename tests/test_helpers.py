import bootstrap  # noqa


def test_getrusage():
    from markii.markii import getrusage

    try:
        import resource  # noqa
        assert getrusage()
    except ImportError:
        assert getrusage() is None


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
