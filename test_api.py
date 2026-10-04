import os


os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

os.environ["SECRET_KEY"] = (
    "test-secret"
)

os.environ["GEMINI_API_KEY"] = ""


from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_register_home_history():

    email = "testuser@example.com"


    response = client.post(

        "/api/auth/register",

        json={

            "name":
                "Test User",

            "email":
                email,

            "password":
                "secret123"
        }
    )


    if response.status_code == 409:

        response = client.post(

            "/api/auth/login",

            json={

                "email":
                    email,

                "password":
                    "secret123"
            }
        )


    assert response.status_code == 200


    response = client.post(

        "/api/generate-home",

        json={

            "budget":
                50000,

            "room_type":
                "Living Room",

            "style":
                "modern",

            "items":
                {},

            "city":
                "Chennai"
        }
    )


    assert response.status_code == 200

    assert (
        response.json()["source"]
        == "fallback"
    )


    history_response = client.get(
        "/api/history"
    )


    assert (
        history_response.status_code
        == 200
    )


def test_party():

    response = client.post(

        "/api/generate-party",

        json={

            "budget":
                20000,

            "guests":
                20,

            "event_type":
                "Birthday",

            "venue":
                "Home",

            "city":
                "Chennai"
        }
    )


    assert response.status_code == 200