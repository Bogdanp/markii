# markii

MarkII is a development-mode error handler for Python web applications.

[![Build Status](https://travis-ci.org/Bogdanp/markii.svg?branch=master)](https://travis-ci.org/Bogdanp/markii)
[![Coverage Status](https://coveralls.io/repos/Bogdanp/markii/badge.svg?branch=master&service=github)](https://coveralls.io/github/Bogdanp/markii?branch=master)
[![Codacy Badge](https://api.codacy.com/project/badge/grade/e4f8f67831224812ba086e09226b203b)](https://www.codacy.com/app/bogdan/markii)

## Installation

`pip install markii`

## Usage

### falcon

``` python
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
httpserver.serve(app, host="127.0.0.1", port="8080")
```

### webapp2

```python
import webapp2

from functools import partial
from markii.frameworks.webapp2 import handle_error
from paste import httpserver


class Handler(webapp2.RequestHandler):
    def get(self, n):
        self.response.write(str(int(n)))


app = webapp2.WSGIApplication([
    webapp2.Route(r"/<n:.*>", handler=Handler)
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

## Gotchas

On AppEngine, you must call `markii.appengine.fix_appengine()` inside
your error handler.

## Text editor support

MarkII supports opening files in your editor when you double click a
frame by taking advantage of OSX's URL handler feature. See:

- [Emacs](https://github.com/typester/emacs-handler)
- [MacVim](https://code.google.com/p/macvim/issues/detail?id=105)
- [Sublime Text](https://github.com/typester/emacs-handler)


## Acknowledgements

MarkII borrows its ideas (and most of its look) from [better_errors](https://github.com/charliesome/better_errors).
