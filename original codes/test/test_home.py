from fastapi.testclient import TestClient

from carsharing import router

client = TestClient(router)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.text