from flask import session
import pytest

def test_hash_data(client):
    response = client.get("/")
    response_hash_data_post = client.post("/hash_data", data={"data":"password"})
    assert response_hash_data_post.status_code == 200
    assert b"argon2id" in response_hash_data_post.data
