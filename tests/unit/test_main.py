def test_main_page(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome user"}
    assert response.headers["content-type"] == "application/json"

