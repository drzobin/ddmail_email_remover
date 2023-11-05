from flask import current_app
import pytest
import os

def test_hash_data(client):
    response_hash_data_post = client.post("/hash_data", data={"data":"password"})
    assert response_hash_data_post.status_code == 200
    assert b"argon2id" in response_hash_data_post.data

def test_main(client,app):
    response_main_post = client.post("/", data={"password":"password", "domain":"test.se", "email":"test@test.se"})
    assert response_main_post.status_code == 200
    assert b"done" in response_main_post.data

    with app.app_context():
        test_email_folder  = current_app.config["EMAIL_ACCOUNT_PATH"] + "/test.se" + "/test"
        assert os.path.exists(test_email_folder) == False

def test_main_wrong_password(client,app):
    response_main_post = client.post("/", data={"password":"wrongpassword", "domain":"test.se", "email":"test@test.se"})
    assert response_main_post.status_code == 200
    assert b"error: wrong password" in response_main_post.data

    with app.app_context():
        test_email_folder  = current_app.config["EMAIL_ACCOUNT_PATH"] + "/test.se" + "/test"
        assert os.path.exists(test_email_folder) == True

def test_main_illigal_char_email(client,app):
    response_main_post = client.post("/", data={"password":"password", "domain":"test.se", "email":"test@test..se"})
    assert response_main_post.status_code == 200
    assert b"error: email validation failed" in response_main_post.data

    with app.app_context():
        test_email_folder  = current_app.config["EMAIL_ACCOUNT_PATH"] + "/test.se" + "/test"

def test_main_illigal_char_password(client,app):
    response_main_post = client.post("/", data={"password":"..password", "domain":"test.se", "email":"test@test.se"})
    assert response_main_post.status_code == 200
    assert b"error: password validation failed" in response_main_post.data

    with app.app_context():
        test_email_folder  = current_app.config["EMAIL_ACCOUNT_PATH"] + "/test.se" + "/test"

def test_main_illigal_char_domain(client,app):
    response_main_post = client.post("/", data={"password":"password", "domain":"..test.se", "email":"test@test.se"})
    assert response_main_post.status_code == 200
    assert b"error: domain validation failed" in response_main_post.data

    with app.app_context():
        test_email_folder  = current_app.config["EMAIL_ACCOUNT_PATH"] + "/test.se" + "/test"
