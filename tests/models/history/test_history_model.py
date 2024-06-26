import json
from src.models.history_model import HistoryModel


# Req. 7
def test_request_history(prepare_base):
    data = json.loads(HistoryModel.list_as_json())
    assert len(data) == 2
    assert data[0]["text_to_translate"] == "Hello, I like videogame"
    assert data[1]["text_to_translate"] == "Do you love music?"
