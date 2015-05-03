import inspect
import os
import sys

from collections import OrderedDict
from jinja2 import Environment, FileSystemLoader

try:
    import resource
except ImportError:
    resource = None


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


def static(filename):
    return open(rel("static", filename)).read()

STYLE = static("markii.css")
SCRIPT = static("markii.js")
JINJA_LOADER = FileSystemLoader(rel("static"))
JINJA = Environment(loader=JINJA_LOADER)
TEMPLATE = JINJA.get_template("template.html")


def getrusage():
    if resource is None:
        return None

    try:
        return resource.getrusage(resource.RUSAGE_SELF)
    except:
        return None


def deindent(source):
    if source.startswith(" "):
        lines = source.split("\n")
        level = len(filter(lambda s: not s, lines[0].split(" ")))
        return "\n".join(line[level:] for line in lines)

    return source


def getsource(ob):
    try:
        return deindent(inspect.getsource(ob))
    except IOError:
        return None


def dict_to_kv(d):
    return {k: repr(v) for k, v in d.iteritems()}


def build_response(request, frames, exception, process):
    error = exception.__class__.__name__
    message = str(exception)

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


def markii(request, exception):
    _, __, traceback = sys.exc_info()
    items = inspect.getinnerframes(traceback)
    frames = []
    try:
        for item in items:
            frame, filename, line, func, lines, index = item
            f_locals = frame.f_locals
            try:
                lines = [l.strip() for l in lines]
                source = getsource(frame).strip().split("\n")
                source = [(l.strip() in lines, l) for l in source]
                func_locals = dict_to_kv(frame.f_locals)
                instance_locals = None
                if "self" in func_locals:
                    instance = f_locals.get("self")
                    instance_vars = vars(instance)
                    try:
                        instance_locals = dict_to_kv(instance_vars)
                    finally:
                        del instance_vars
                        del instance

                frames.append((
                    func, func_locals, instance_locals,
                    filename, source, line, lines
                ))
            finally:
                del f_locals
                del frame
                del item

        frames = frames[::-1]
        rusage = getrusage()
        process = None
        if rusage is not None:
            process = OrderedDict((
                ("utime", str(rusage.ru_utime)),
                ("stime", str(rusage.ru_stime)),
                ("mem", "{0:.2f}MB".format(float(rusage.ru_maxrss) / 1024 / 1024)),
            ))

        return build_response(request, frames, exception, process)
    finally:
        del frames
        del items
        del traceback
