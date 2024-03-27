import pytest
from flask import url_for

from app.blueprints.conftest import login, logout


@pytest.fixture(scope='module')
def test_client(test_client):
    """
    Extends the test_client fixture to add additional specific data for module testing.
    for module testing (por example, new users)
    """
    with test_client.application.app_context():
        # Add HERE new elements to the database that you want to exist in the test context.
        # DO NOT FORGET to use db.session.add(<element>) and db.session.commit() to save the data.
        pass

    yield test_client


def test_login_success(test_client):
    response = test_client.post('/login', data=dict(
        email='test@example.com',
        password='test1234'
    ), follow_redirects=True)

    assert response.request.path != url_for('auth.login'), "Login was unsuccessful"

    test_client.get('/logout', follow_redirects=True)


def test_login_unsuccessful_bad_email(test_client):
    response = test_client.post('/login', data=dict(
        email='bademail@example.com',
        password='test1234'
    ), follow_redirects=True)

    assert response.request.path == url_for('auth.login'), "Login was unsuccessful"

    test_client.get('/logout', follow_redirects=True)


def test_login_unsuccessful_bad_password(test_client):
    response = test_client.post('/login', data=dict(
        email='test@example.com',
        password='basspassword'
    ), follow_redirects=True)

    assert response.request.path == url_for('auth.login'), "Login was unsuccessful"

    test_client.get('/logout', follow_redirects=True)


def test_edit_profile_page_get(test_client):
    """
    Tests access to the profile editing page via a GET request.
    """
    login_response = login(test_client, 'test@example.com', 'test1234')
    assert login_response.status_code == 200, "Login was unsuccessful."

    response = test_client.get('/profile/edit')
    assert response.status_code == 200, "The profile editing page could not be accessed."
    assert b"Edit profile" in response.data, "The expected content is not present on the page"

    logout(test_client)
