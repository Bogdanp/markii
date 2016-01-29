from collections import OrderedDict

from .. import markii


def handle_error(request, response, exception, code=500, app_root=""):
    response.write(markii(exception, request=OrderedDict((
        ("url", request.url),
        ("query_string", request.query_string),
        ("method", request.method),
        ("cookies", request.cookies),
        ("headers", request.headers),
        ("params", request.params or {}),
        ("body", request.body),
    )), app_root=app_root))
    response.set_status(code)
