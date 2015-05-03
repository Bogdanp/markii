# markii

MarkII is an improved development-mode error handler for Python web
applications. Currently the only supported framework is `webapp2`.

## Installation

`$ pip install markii`

## Usage

In your `main.py` file:

```python
from functools import partial
from markii.frameworks.webapp2 import handle_error

app = webapp2.WSGIApplication(routes)
app.error_handlers[400] = partial(handle_error, code=400)
app.error_handlers[404] = partial(handle_error, code=404)
app.error_handlers[500] = partial(handle_error, code=500)
app.run()
```

## Screenshot

![/example/screenshot.png]

## Warning

Make sure you only use MarkII in development mode.

## Acknowledgements

MarkII borrows its ideas (and most of its look) from [better_errors](https://github.com/charliesome/better_errors).
