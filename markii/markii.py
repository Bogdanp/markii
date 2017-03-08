import base64
import inspect
import os
import six
import sys

from collections import OrderedDict, namedtuple
from jinja2 import Environment, FileSystemLoader

try:
    import resource
except ImportError:  # pragma: no cover
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
JINJA = Environment(loader=JINJA_LOADER, autoescape=True)
TEMPLATE = JINJA.get_template("template.html")


def deindent(source):
    if source.startswith(" "):
        lines = source.split("\n")  # ["  pass", ...]
        chars = lines[0].split(" ")  # ["", "", "pass"]
        level = sum(not c for c in chars)  # 2
        return "\n".join(line[level:] for line in lines)

    return source


def dict_to_kv(d):
    return {k: repr(v) for k, v in six.iteritems(d)}


_ascii_range = range(0, 128)


def _b2i(b):
    if isinstance(b, six.integer_types):
        return b
    return ord(b)


def sanitize(d):
    """Ensures that all values inside of the given dictionary are
    represent valid ascii.  Child dictionaries are sanitized
    recursively.

    :param dict d:
      The input dictionary.
    :returns dict:
      The sanitized dictionary.
    """
    if d is None:
        return d

    sanitized_d = {}
    for key, value in six.iteritems(d):
        if isinstance(value, dict):
            sanitized_d[key] = sanitize(value)

        elif isinstance(value, six.text_type):
            sanitized_d[key] = value.encode("utf8", errors="replace")

        else:
            value = six.binary_type(value)

            if all(_b2i(b) not in _ascii_range for b in value):
                sanitized_d[key] = base64.b64encode(value)
            else:
                sanitized_d[key] = value

    return sanitized_d


def getrusage():
    if resource is None:
        return None

    try:
        return resource.getrusage(resource.RUSAGE_SELF)
    except (ValueError, resource.error):  # pragma: no cover
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
        source = deindent(inspect.getsource(ob))
        if isinstance(source, six.binary_type):
            source = source.decode("utf-8")

        return source.strip().split("\n")
    except BaseException:
        return ""


def getframes(app_root=""):
    _, _, traceback = sys.exc_info()
    items = inspect.getinnerframes(traceback)
    frames = []
    try:
        for item in items:
            frame, filename, line, func, lines, _ = item
            app_local = filename.startswith(app_root)
            f_locals = frame.f_locals
            try:
                lines = [l.strip() for l in lines or []]
                source = ((l.strip() in lines, l) for l in getsource(frame))
                func_locals = dict_to_kv(frame.f_locals)
                instance_class = None
                instance_locals = None
                if "self" in func_locals:
                    instance = f_locals.get("self")
                    instance_class = instance.__class__.__name__
                    instance_vars = {}

                    if hasattr(instance, "__dict__"):
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
    message = six.text_type(exception)
    frames = getframes(app_root)
    process = getprocinfo()
    return TEMPLATE.render(
        style=STYLE,
        script=SCRIPT,
        error=error,
        message=message,
        frames=frames,
        request=sanitize(request),
        process=process,
        hasattr=hasattr,
        ismethod=inspect.ismethod
    )
