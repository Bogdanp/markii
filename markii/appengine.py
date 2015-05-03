import sys


class fix_appengine(object):
    "Works around the GAE ``inspect.getouterframes`` issue."

    def __init__(self):
        sys.modules["__main__"] = self

    def __getattr__(self, name):
        return globals()[name]
