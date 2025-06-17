from flask import current_app
import pytest
import os


def test_main_wrong_password(client, app):
    """Test authentication with incorrect password

    This test verifies that the application correctly rejects requests with an
    incorrect password. The endpoint should return a 200 status code with a
    specific error message indicating the password was wrong.
    """
    response_main_post = client.post("/", data={"password":"wrongpassword", "domain":"test.se", "email":"test@test.se"})
    assert response_main_post.status_code == 200
    assert b"error: wrong password" in response_main_post.data


def test_main_illigal_char_email(client, app, password):
    """Test email validation failure

    This test verifies that the application properly validates the email parameter
    and rejects requests containing invalid email formats. The endpoint should
    return a specific error message indicating the email validation failed.
    """
    response_main_post = client.post("/", data={"password":password, "domain":"test.se", "email":"test@test..se"})
    assert response_main_post.status_code == 200
    assert b"error: email validation failed" in response_main_post.data


def test_main_illigal_char_password(client, app):
    """Test password validation failure

    This test verifies that the application properly validates the password parameter
    and rejects requests containing invalid password formats. The endpoint should
    return a specific error message indicating the password validation failed.
    """
    response_main_post = client.post("/", data={"password":"..password", "domain":"test.se", "email":"test@test.se"})
    assert response_main_post.status_code == 200
    assert b"error: password validation failed" in response_main_post.data


def test_main_illigal_char_domain(client, app, password):
    """Test domain validation failure

    This test verifies that the application properly validates the domain parameter
    and rejects requests containing invalid domain formats. The endpoint should
    return a specific error message indicating the domain validation failed.
    """
    response_main_post = client.post("/", data={"password":password, "domain":"..test.se", "email":"test@test.se"})
    assert response_main_post.status_code == 200
    assert b"error: domain validation failed" in response_main_post.data


def test_main_not_matching_domain(client, app, password):
    """Test email and domain matching validation

    This test verifies that the application properly validates that the email domain
    matches the specified domain parameter. The endpoint should return a specific
    error message when the email address domain does not match the provided domain.
    """
    response_main_post = client.post("/", data={"password":password, "domain":"test.se", "email":"test@testtest.se"})
    assert response_main_post.status_code == 200
    assert b"error: email adress domain do not match domain" in response_main_post.data
