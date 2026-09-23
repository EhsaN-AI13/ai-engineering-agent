from unittest.mock import Mock, patch
from api import get_agent

from fastapi.testclient import TestClient

from api import app, get_agent


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "EhsaN AI Agent API is running."
    }


def test_chat():
    mock_agent = Mock()

    mock_agent.run.return_value = "۵۰"

    def override_get_agent():
        return mock_agent

    app.dependency_overrides[get_agent] = override_get_agent

    response = client.post(
        "/chat",
        json={
            "message": "10 ضربدر 5 چند میشه؟"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "response": "۵۰"
    }

    mock_agent.run.assert_called_once_with(
        "10 ضربدر 5 چند میشه؟"
    )

    app.dependency_overrides.clear()

def test_chat_dependency_injection():
    mock_agent = Mock()

    mock_agent.run.return_value = "Hello from mock agent"

    def override_get_agent():
        return mock_agent

    app.dependency_overrides[get_agent] = override_get_agent

    response = client.post(
        "/chat",
        json={
            "message": "Hello"
        }
    )

    assert response.status_code == 200

    assert response.json() == {
        "response": "Hello from mock agent"
    }

    mock_agent.run.assert_called_once_with("Hello")

    app.dependency_overrides.clear()

def test_chat_empty_message():
    response = client.post(
        "/chat",
        json={
            "message": ""
        }
    )

    assert response.status_code == 422


def test_chat_invalid_message_type():
    response = client.post(
        "/chat",
        json={
            "message": 123
        }
    )

    assert response.status_code == 422

def test_chat_agent_error():
    mock_agent = Mock()

    mock_agent.run.side_effect = Exception("Something went wrong")

    app.state.agent = mock_agent

    response = client.post(
        "/chat",
        json={
            "message": "Hello"
        }
    )

    assert response.status_code == 500

    assert response.json() == {
        "detail": "An internal error occurred."
    }

def test_chat_invalid_response():
    mock_agent = Mock()

    mock_agent.run.return_value = {
        "wrong_field": "hello"
    }

    app.state.agent = mock_agent

    client = TestClient(
        app,
        raise_server_exceptions=False
    )

    response = client.post(
        "/chat",
        json={
            "message": "Hello"
        }
    )

    assert response.status_code == 500

def test_agent_created_once():
    mock_agent = Mock()

    with patch(
        "api.create_agent",
        return_value=mock_agent
    ) as mock_create_agent:

        with TestClient(app):
            assert app.state.agent is mock_agent

        mock_create_agent.assert_called_once()

def test_agent_cleanup():
    mock_agent = Mock()

    with patch(
        "api.create_agent",
        return_value=mock_agent
    ):

        with TestClient(app):
            assert app.state.agent is mock_agent

        assert app.state.agent is None

def test_agent_shared_between_requests():
    mock_agent = Mock()

    mock_agent.run.side_effect = [
        "پاسخ اول",
        "پاسخ دوم"
    ]

    def override_get_agent():
        return mock_agent

    app.dependency_overrides[get_agent] = override_get_agent

    response_1 = client.post(
        "/chat",
        json={
            "message": "سلام"
        }
    )

    response_2 = client.post(
        "/chat",
        json={
            "message": "حالت چطوره؟"
        }
    )

    assert response_1.status_code == 200
    assert response_2.status_code == 200

    assert response_1.json() == {
        "response": "پاسخ اول"
    }

    assert response_2.json() == {
        "response": "پاسخ دوم"
    }

    assert mock_agent.run.call_count == 2

    mock_agent.run.assert_any_call("سلام")
    mock_agent.run.assert_any_call("حالت چطوره؟")

    app.dependency_overrides.clear()