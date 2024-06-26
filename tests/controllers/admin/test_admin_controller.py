import json
import pytest
from src.database.db import db
from src.models.history_model import HistoryModel
from src.models.user_model import UserModel


@pytest.fixture(autouse=True)
def create_user():
    db.get_collection("users").drop()
    UserModel({
        "name": "Peter",
        "level": "admin",
        "token": "token_secreto123"
    }).save()


def test_history_delete(app_test):
    histories = json.loads(HistoryModel.list_as_json())

    assert len(histories) == 2
    assert histories[0]["text_to_translate"] == "Hello, I like videogame"
    assert histories[1]["text_to_translate"] == "Do you love music?"

    history = HistoryModel.find_one({
        "text_to_translate": "Hello, I like videogame"
    })
    id = str(history.data["_id"])

    app_test.delete(
        f"/admin/history/{id}",
        headers={
            "Authorization": "token_secreto123",
            "User": "Peter",
        }
    )

    histories = json.loads(HistoryModel.list_as_json())

    assert len(histories) == 1
    assert histories[0]["text_to_translate"] == "Do you love music?"


def test_history_delete_fail_empty_user(app_test):
    response = app_test.delete(
        f"/admin/history/{id}",
        headers={
            "Authorization": "token_secreto123",
            "User": "Paula",
        }
    )

    assert response.status_code == 401
    assert "Unauthorized Access" in response.text
