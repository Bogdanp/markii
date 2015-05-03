from markii import markii
from markii.appengine import fix_appengine

from collections import OrderedDict


def handle_error(request, response, exception, code=500):
    fix_appengine()
    request = OrderedDict((
        ("url", request.url),
        ("query_string", request.query_string),
        ("method", request.method),
        ("cookies", request.cookies),
        ("headers", request.headers),
        ("params", request.params or {}),
        ("body", request.body),
    ))
    response.write(markii(request, exception))
    response.set_status(code)
