import six

from example.falcon_app import app
from falcon.testing import TestBase


class TestFalconErrors(TestBase):
    def setUp(self):
        super(TestFalconErrors, self).setUp()
        self.api = app

    def test_happy_path(self):
        body = self.simulate_request("/1")
        self.assertEqual(body, [six.b("1")])
        self.assertEqual(self.srmock.status, "200 OK")

    def test_error(self):
        body = self.simulate_request("/")
        self.assertIn(six.b("invalid literal for int()"), body[0])
        self.assertEqual(self.srmock.status, "500 Internal Server Error")
