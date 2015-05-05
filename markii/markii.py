import inspect
import os
import sys

from collections import OrderedDict, namedtuple
from jinja2 import Environment, FileSystemLoader

try:
    import resource
except ImportError:
    resource = None


Frame = namedtuple("Frame", [
    "func", "func_locals", "instance_class", "instance_locals",
    "filename", "source", "line", "lines", "app_local"
])


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


def static(filename):
    return open(rel("static", filename)).read()

STYLE = static("markii.css")
SCRIPT = static("markii.js")
JINJA_LOADER = FileSystemLoader(rel("static"))
JINJA = Environment(loader=JINJA_LOADER)
TEMPLATE = JINJA.get_template("template.html")


def deindent(source):
    if source.startswith(" "):
        lines = source.split("\n")
        level = len(filter(lambda s: not s, lines[0].split(" ")))
        return "\n".join(line[level:] for line in lines)

    return source


def dict_to_kv(d):
    return {k: repr(v) for k, v in d.iteritems()}


def getrusage():
    if resource is None:
        return None

    try:
        return resource.getrusage(resource.RUSAGE_SELF)
    except:
        return None


def getprocinfo():
    rusage = getrusage()
    if rusage is None:
        return None

    return OrderedDict((
        ("utime", str(rusage.ru_utime)),
        ("stime", str(rusage.ru_stime)),
        ("mem", "{0:.2f}MB".format(float(rusage.ru_maxrss) / 1024 / 1024)),
    ))


def getsource(ob):
    try:
        return deindent(inspect.getsource(ob))
    except Exception:
        return ""


def getframes(app_root=""):
    _, __, traceback = sys.exc_info()
    items = inspect.getinnerframes(traceback)
    frames = []
    try:
        for item in items:
            frame, filename, line, func, lines, index = item
            app_local = filename.startswith(app_root)
            f_locals = frame.f_locals
            try:
                lines = [l.strip() for l in lines]
                source = getsource(frame).strip().split("\n")
                source = [(l.strip() in lines, l) for l in source]
                func_locals = dict_to_kv(frame.f_locals)
                instance_class = None
                instance_locals = None
                if "self" in func_locals:
                    instance = f_locals.get("self")
                    instance_class = instance.__class__.__name__
                    instance_vars = vars(instance)
                    try:
                        instance_locals = dict_to_kv(instance_vars)
                    finally:
                        del instance_vars
                        del instance
                elif "cls" in func_locals:
                    clazz = f_locals.get("cls")
                    if inspect.isclass(clazz):
                        instance_class = clazz.__name__

                frames.append(Frame(
                    func, func_locals, instance_class, instance_locals,
                    filename, source, line, lines, app_local
                ))
            finally:
                del f_locals
                del frame
                del item

        return frames[::-1]
    finally:
        del frames
        del items
        del traceback


def markii(exception, request=None, app_root=""):
    """Inspects the current exception and generates a static HTML dump
    with its frame information.

    :param Exception exception:
      The exception being inspected.
    :param dict request:
      A dict containing information about the request.
    :param str app_root:
      The app's root path. This is used to determine which frames
      belong to the app and which don't.
    :returns:
      The generated HTML as a str.
    """
    error = exception.__class__.__name__
    message = str(exception)
    frames = getframes(app_root)
    process = getprocinfo()
    return TEMPLATE.render(
        style=STYLE,
        script=SCRIPT,
        error=error,
        message=message,
        frames=frames,
        request=request,
        process=process,
        hasattr=hasattr,
        ismethod=inspect.ismethod
    )
