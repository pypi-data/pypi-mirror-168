from openwebpos import open_web_pos


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check that the response is valid
    """

    flask_app = open_web_pos()

    # create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('/')
        assert response.status_code == 302


def test_login_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the '/login' page is requested (GET)
    THEN check that the response is valid
    """

    flask_app = open_web_pos()

    # create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get('user/login')
        assert response.status_code == 200
