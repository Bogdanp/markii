import falcon
import os

from functools import partial
from markii.frameworks.falcon import handle_error
from paste import httpserver


class Handler(object):
    def on_get(self, request, response, n):
        response.body = str(int(n))


root = os.path.abspath(os.path.dirname(__file__))
app = falcon.API()
app.add_error_handler(Exception, partial(handle_error, app_root=root))
app.add_route("/{n}", Handler())

if __name__ == "__main__":
    httpserver.serve(app, host="127.0.0.1", port="8080")
