# EhSaN AI Agent

An extensible AI Agent built with Python, FastAPI, OpenAI, custom tools, conversation memory, automated evaluation, testing, GitHub Actions CI, Docker, and request tracing.

**EhSaN** demonstrates practical AI Engineering concepts including agent orchestration, tool calling, API development, observability, automated testing, evaluation, and containerization.

---

## 🚀 Features

- 🤖 AI Agent architecture
- 🧠 Conversation memory
- 🛠️ Custom tool system
- 🔢 Calculator tool
- 📝 Word counting tool
- 🕒 Current time tool
- 📄 File reader tool
- 🔎 Web search integration through the LLM Responses API
- 🔧 Tool Registry and Tool Executor
- ⚡ FastAPI REST API
- 🩺 Health Check endpoint
- 🆔 Request ID generation
- 🔍 Request tracing
- ⏱️ Request duration logging
- 📝 Structured application logging
- 🧪 Automated testing with Pytest
- 📊 Agent evaluation framework
- 🐳 Docker support
- 🔄 GitHub Actions CI
- 🛡️ Error handling
- ⚙️ Environment-based configuration

---

## 🏗️ Architecture

```text
                         ┌─────────────────┐
                         │      User       │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    FastAPI      │
                         │   REST API      │
                         └────────┬────────┘
                                  │
                         Request ID Middleware
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     EhSaN       │
                         │   AI Agent      │
                         └────────┬────────┘
                                  │
                ┌─────────────────┼─────────────────┐
                │                 │                 │
                ▼                 ▼                 ▼
        ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
        │ Conversation │  │     LLM      │  │ Tool Registry│
        │    Memory    │  │              │  │              │
        └──────────────┘  └──────┬───────┘  └──────┬───────┘
                                 │                 │
                                 │ Tool Call       │
                                 └────────┬────────┘
                                          ▼
                                  ┌───────────────┐
                                  │ Tool Executor │
                                  └───────┬───────┘
                                          │
                                          ▼
                                  ┌───────────────┐
                                  │  Tool Result  │
                                  └───────┬───────┘
                                          │
                                          ▼
                                  ┌───────────────┐
                                  │  LLM Response │
                                  └───────┬───────┘
                                          │
                                          ▼
                                       User
```

### Core Components

- **EhSaN Agent** — Main agent interface and orchestration layer.
- **LLM** — Handles communication with the language model and tool-calling flow.
- **Conversation Memory** — Stores conversation history.
- **Tool Registry** — Registers available tools and their definitions.
- **Tool Executor** — Executes tools requested by the agent.
- **FastAPI** — Provides the REST API.
- **Evaluation** — Measures agent behavior against predefined test cases.
- **Docker** — Provides a reproducible containerized environment.
- **GitHub Actions** — Runs the automated test suite on pushes and pull requests.

---

## 🛠️ Available Tools

| Tool | Description |
|---|---|
| `calculator` | Performs basic arithmetic operations |
| `count_words` | Counts words in a text |
| `get_current_time` | Returns the current local time |
| `read_file` | Reads UTF-8 text files |
| `web_search` | Enables web search through the LLM's web-search capability |

> The `tools/web_search.py` module is retained as part of the project's tool structure, while the active web-search capability is provided through the LLM integration.

---

## 🔍 Request Tracing & Observability

Each incoming HTTP request receives a unique UUID.

The identifier is returned through the `X-Request-ID` response header and propagated through the application using Python's `ContextVar`.

Example:

```text
2026-09-23 20:22:05 - INFO -
[request_id=1a0aac29-7463-4637-8e20-9996307ea08a] -
Request started

2026-09-23 20:22:05 - INFO -
[request_id=1a0aac29-7463-4637-8e20-9996307ea08a] -
Request finished | status_code=200 | duration=0.0014s
```

This allows individual API requests to be correlated with application logs.

---

## 📡 API

### Root

```http
GET /
```

Response:

```json
{
  "message": "EhsaN AI Agent API is running."
}
```

### Health Check

```http
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "agent": "EhSaN",
  "model": "gpt-5.6-luna",
  "environment": "development"
}
```

### Chat

```http
POST /chat
```

Request:

```json
{
  "message": "What is 25 multiplied by 4?"
}
```

Response:

```json
{
  "response": "100"
}
```

Every HTTP request also receives an `X-Request-ID` response header.

Interactive Swagger documentation is available at `/docs`.

---

## 📁 Project Structure

```text
ai-engineering-agent/
│
├── agent/
│   ├── __init__.py
│   ├── agent.py
│   ├── llm.py
│   ├── memory.py
│   ├── tool_executor.py
│   ├── tool_registry.py
│   └── tool_selector.py
│
├── tools/
│   ├── __init__.py
│   ├── calculator.py
│   ├── text_tool.py
│   ├── datetime_tool.py
│   ├── definitions.py
│   ├── file_reader.py
│   └── web_search.py
│
├── evaluation/
│   ├── __init__.py
│   ├── evaluator.py
│   ├── cases.py
│   ├── mock_agent.py
│   ├── run_evaluation.py
│   └── test_evaluator.py
│
├── tests/
│   ├── test_agent.py
│   ├── test_api.py
│   ├── test_agent_factory.py
│   ├── test_config.py
│   └── test_logger.py
│
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── api.py
├── agent_factory.py
├── config.py
├── logger.py
├── Dockerfile
├── requirements.txt
├── pytest.ini
├── README.md
└── .gitignore
```

---

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/EhSaN-AI13/ai-engineering-agent.git
cd ai-engineering-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 🔐 Environment Configuration

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-5.6-luna
ENVIRONMENT=development
```

Configuration defaults:

| Variable | Default |
|---|---|
| `OPENAI_API_KEY` | None |
| `OPENAI_MODEL` | `gpt-5.6-luna` |
| `ENVIRONMENT` | `development` |

> Never commit `.env` files or API keys to GitHub.

---

## ▶️ Running the API

Start the FastAPI application:

```bash
uvicorn api:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## 🧪 Testing

The project uses Pytest for automated testing.

Run the complete test suite:

```bash
python -m pytest
```

Current verified test suite:

```text
86 passed
```

The tests cover:

- Agent behavior
- Tool execution
- Tool registry
- API endpoints
- Dependency injection
- Error handling
- Request IDs
- Request logging
- Request ID propagation
- Configuration
- Logging
- Agent evaluation

---

## 📊 Evaluation

The project includes a dedicated evaluation framework:

```text
evaluation/
├── evaluator.py
├── cases.py
├── mock_agent.py
└── run_evaluation.py
```

The evaluation system tests agent behavior against predefined scenarios independently from the live LLM service.

---

## 🐳 Docker

Build the Docker image:

```bash
docker build -t ehsan-ai-agent .
```

Run the container:

```bash
docker run --name ehsan-ai-agent-container -p 8000:8000 --env-file .env ehsan-ai-agent
```

The API will be available at `http://127.0.0.1:8000`.

Health check:

```text
http://127.0.0.1:8000/health
```

The containerized application has been verified with the API health check and request-tracing system.

---

## 🔄 GitHub Actions CI

The project uses GitHub Actions for continuous integration.

The workflow runs on:

- Pushes
- Pull requests

The CI pipeline:

1. Checks out the repository
2. Sets up Python 3.14
3. Installs project dependencies
4. Runs the Pytest test suite

Workflow:

```text
.github/
└── workflows/
    └── ci.yml
```

---

## 🧠 Engineering Concepts Demonstrated

This project demonstrates practical implementation of:

- Python software architecture
- Object-oriented design
- LLM integration
- AI Agent architecture
- Tool calling
- Function definitions
- Conversation memory
- REST API development
- FastAPI dependency injection
- Request tracing
- Structured logging
- Error handling
- Automated testing
- Agent evaluation
- Configuration management
- Docker containerization
- Continuous Integration

---

## 📌 Project Status

**Status: Active Portfolio Project**

Implemented:

- AI Agent core
- Tool system
- Conversation memory
- LLM integration
- FastAPI API
- Health check
- Request tracing
- Structured logging
- Automated testing
- Evaluation framework
- Docker
- GitHub Actions CI

---

## 👨‍💻 Author

**EhSaN**

GitHub: https://github.com/EhSaN-AI13
