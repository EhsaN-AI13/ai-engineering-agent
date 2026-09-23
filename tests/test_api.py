from unittest.mock import Mock, patch

from fastapi.testclient import TestClient

from api import app, get_agent


client = TestClient(app, raise_server_exceptions=False)


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
    with TestClient(app):
        response = client.post(
            "/chat",
            json={
                "message": ""
            }
        )

    assert response.status_code == 422


def test_chat_invalid_message_type():
    with TestClient(app):
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

def test_health():
    with TestClient(app):
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
    "status": "healthy",
    "agent": "EhSaN",
    "model": "gpt-5.6-luna",
    "environment": "development"
    }
     
def test_request_id_header():
    with TestClient(app):
        response = client.get("/")

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]

def test_request_id_is_unique():
    with TestClient(app):
        response_1 = client.get("/")
        response_2 = client.get("/")

    request_id_1 = response_1.headers["X-Request-ID"]
    request_id_2 = response_2.headers["X-Request-ID"]

    assert request_id_1 != request_id_2

def test_request_logging(caplog):
    with TestClient(app):
        response = client.get("/health")

    assert response.status_code == 200

    logs = caplog.text

    assert "Request started" in logs
    assert "Request finished" in logs
    assert "request_id=" in logs
    assert "duration=" in logs
   

def test_request_id_propagates_to_agent_logs(caplog):
    mock_response = Mock()
    mock_response.output = []
    mock_response.output_text = "Mock response"

    mock_openai = Mock()
    mock_openai.responses.create.return_value = mock_response

    with patch(
        "agent.llm.OpenAI",
        return_value=mock_openai
    ), patch(
        "agent.llm.settings.OPENAI_API_KEY",
        "test-key"
    ):
        with TestClient(app) as client:
            response = client.post(
                "/chat",
                json={"message": "Hello"}
            )

    assert response.status_code == 200

    logs = caplog.text

    start_line = next(
        line for line in logs.splitlines()
        if "Request started" in line
    )

    request_id = start_line.split("request_id=")[1].split()[0]

    assert request_id != "-"

    assert "Agent started." in logs
    assert "LLM request started." in logs

    assert f"request_id={request_id}" in start_line

def test_request_id_does_not_leak_between_requests(caplog):
    with TestClient(app) as client:
        response_1 = client.get("/")
        response_2 = client.get("/")

    request_id_1 = response_1.headers["X-Request-ID"]
    request_id_2 = response_2.headers["X-Request-ID"]

    assert request_id_1 != request_id_2
    assert request_id_1 != "-"
    assert request_id_2 != "-"