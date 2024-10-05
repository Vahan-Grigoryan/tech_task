from ....core.tests.client import client

def test_required_fields():
    response = client.post("/registration")
    assert response.status_code == 400
    assert response.json() == {
        "detail": [
            {
                "field": "email",
                "message": "Field required"
            },
            {
                "field": "password",
                "message": "Field required"
            }
        ]
    }

def test_email_validation():
    testing_data = ("JAKL", "jart@mailskwijieuuwqi.com","test_mail_example@mail.ru")
    other_fields = {
        "password":"testing_data_password9876543I",
    }
    responses =  []

    for email in testing_data:
        response = client.post(
            "/registration",
            data={"email": email, **other_fields}
        )
        responses.append(response)

    assert all((
        responses[0].status_code == responses[1].status_code == 400,
        responses[0].json()["detail"][0].get("message") == "An email address must have an @-sign.",
        responses[1].json()["detail"][0].get("message") == "The domain name mailskwijieuuwqi.com does not exist.",
        responses[2].status_code == 200,
    ))


def test_password_validation():
    testing_data = (
        "ytrert",
        "gart23aiopaw",
        "gart23aiIopaw"
    )
    other_fields = {
        "email": "ex@mail.ru",
    }
    responses = []

    for password in testing_data:
        response = client.post(
            "/registration",
            data={"password": password, **other_fields}
        )
        responses.append(response)

    assert all((
        responses[0].status_code == responses[1].status_code == 400,
        responses[0].json()["detail"][0].get("message") == "String should have at least 8 characters",
        responses[1].json()["detail"][0].get("message") == "Password should have at least 1 number, lowercase and uppercase letter",
        responses[2].status_code == 200,
    ))
