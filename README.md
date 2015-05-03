# markii

MarkII is an improved development-mode error handler for Python web
applications. Currently the only supported framework is `webapp2`.

## Installation

`$ pip install markii`

## Usage

In your `main.py` file:

```python
import webapp2

from functools import partial
from markii.frameworks.webapp2 import handle_error
from paste import httpserver


class BrokenHandler(webapp2.RequestHandler):
    def get(self, n):
        self.response.write(str(int(n)))


app = webapp2.WSGIApplication([
    webapp2.Route(r"/<n:.*>", handler=BrokenHandler)
], debug=True)
app.error_handlers[400] = partial(handle_error, code=400)
app.error_handlers[404] = partial(handle_error, code=404)
app.error_handlers[500] = partial(handle_error, code=500)
httpserver.serve(app, host="127.0.0.1", port="8080")
```

## Screenshot

![Screenshot](/example/screenshot.png)

## Warning

Make sure you only use MarkII in development mode.

## Acknowledgements

MarkII borrows its ideas (and most of its look) from [better_errors](https://github.com/charliesome/better_errors).
