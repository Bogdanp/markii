import dominate
import inspect
import os
import sys

from dominate.tags import *

from .appengine import fix_appengine


def rel(*xs):
    return os.path.join(os.path.abspath(os.path.dirname(__file__)), *xs)


def static(filename):
    return open(rel("static", filename)).read()


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


def dict_to_table(d, *args, **kwargs):
    t = table(*args, **kwargs)
    for name, value in d.items():
        if name is None:
            continue

        row = tr()
        row.add(td(strong(pre(name))))

        if value and isinstance(value, basestring):
            row.add(td(pre(value)))
        elif value and hasattr(value, "items") and inspect.ismethod(value.items):
            row.add(td(dict_to_table(value, *args, **kwargs)))
        else:
            row.add(td(pre(repr(value))))

        t.add(row)
    return t


def build_response(request, frames, exception):
    title = "Error!"
    message = str(exception)
    if message:
        title = "Error: {}".format(message)

    template = dominate.document(title=title)
    with template.head:
        script(src="https://ajax.googleapis.com/ajax/libs/jquery/2.1.3/jquery.min.js")

    with template:
        with div(id="body"):
            with div(id="exception"):
                h5(str(exception.__class__.__name__))
                h2(str(exception))

            with div(id="lhs"):
                with ul(id="frames"):
                    for i, (func, _, _, filename, _, line, _) in enumerate(frames):
                        with li(cls="func", data_frame=i):
                            h4("{}()".format(func))
                            with h6():
                                span("in {}, line ".format(filename))
                                strong(line)

            with div(id="rhs"):
                for i, (func, locals_, instance_locals, filename, source, line, lines) in enumerate(frames):
                    with div(cls="frame", data_frame=i):
                        if source is not None:
                            lines = [line.strip() for line in lines]
                            with div(cls="section"):
                                h4("Source")
                                with div(cls="source"):
                                    for line in source.strip().split("\n"):
                                        if not line:
                                            br()

                                        if line.strip() in lines:
                                            pre(strong(line))
                                        else:
                                            pre(line)

                        with div(cls="section"):
                            h4("Locals")
                            with dict_to_table(locals_):
                                pass

                        if instance_locals:
                            with div(cls="section"):
                                h4("Instance")
                                with dict_to_table(instance_locals):
                                    pass

                        with div(cls="section"):
                            h4("Request")
                            with dict_to_table(request):
                                pass

    template = str(template)
    template = template.replace("</head>", """
        <style>{css}</style>
        <script>{js}</script>
    </head>""".format(
        css=static("markii.css"),
        js=static("markii.js")
    ))
    return template


def markii(request, exception):
    fix_appengine()
    _, __, traceback = sys.exc_info()
    items = list(reversed(inspect.getinnerframes(traceback)))
    frames = []
    for item in items:
        frame, filename, line, func, lines, index = item
        source = getsource(frame)
        locals_ = frame.f_locals
        instance_locals = None
        if "self" in locals_:
            instance_locals = vars(locals_["self"])

        frames.append((func, locals_, instance_locals, filename, source, line, lines))

    return build_response(request, frames, exception)
