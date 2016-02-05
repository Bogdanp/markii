import pytest
import six


@pytest.mark.skipif(six.PY3, reason="webapp2")
def test_happy_path():
    import webapp2
    from example.webapp2_app import app

    request = webapp2.Request.blank("/1")
    response = request.get_response(app)
    assert response.body == "1"
    assert response.status_int == 200


@pytest.mark.skipif(six.PY3, reason="webapp2")
def test_error():
    import webapp2
    from example.webapp2_app import app

    request = webapp2.Request.blank("/")
    response = request.get_response(app)
    assert "invalid literal for int()" in response.body
    assert response.status_int == 500
