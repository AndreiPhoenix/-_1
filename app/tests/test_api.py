from fastapi import status

def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["title"] == "Test Task"
