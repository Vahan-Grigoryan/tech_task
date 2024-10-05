from ....core.tests.client import client


def test_required_fields():
    response = client.post("/tokens")
    assert response.json() == {
        "detail": [
            {
                "field": "username",
                "message": "Field required"
            },
            {
                "field": "password",
                "message": "Field required"
            }
        ]
    }
