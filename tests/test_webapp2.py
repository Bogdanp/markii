import webapp2

from example.webapp2_app import app


def test_happy_path():
    request = webapp2.Request.blank("/1")
    response = request.get_response(app)
    assert response.body == "1"
    assert response.status_int == 200


def test_error():
    request = webapp2.Request.blank("/")
    response = request.get_response(app)
    assert "invalid literal for int()" in response.body
    assert response.status_int == 500
