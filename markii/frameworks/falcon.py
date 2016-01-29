from __future__ import absolute_import

from collections import OrderedDict
from falcon import HTTP_500

from .. import markii


def handle_error(exception, request, response, params, app_root=""):
    response.content_type = "text/html"
    response.status = HTTP_500
    response.body = markii(exception, request=OrderedDict((
        ("url", request.url),
        ("query_string", request.query_string),
        ("method", request.method),
        ("cookies", request.cookies),
        ("headers", request.headers),
        ("params", request.params or {}),
        ("body", request.stream.read()),
    )), app_root=app_root)
