# EhSaN AI Agent

An AI Agent built with Python, FastAPI, OpenAI, custom tools, conversation memory, automated evaluation, testing, CI/CD, and Docker.

EhSaN is designed as an extensible AI Agent capable of understanding user requests, selecting and executing tools, maintaining conversation memory, and returning the final response.

## Features

* 🤖 AI Agent architecture
* 🧠 Conversation memory
* 🛠️ Custom tool system
* 🔢 Calculator tool
* 📝 Word counting tool
* 🕒 Current time tool
* 📄 File reader tool
* 🔎 Web search integration
* ⚡ FastAPI REST API
* 🧪 Automated testing with Pytest
* 📊 Agent evaluation system
* 🐳 Docker support
* 🔄 GitHub Actions CI
* 📝 Structured logging
* 🛡️ Error handling

## Architecture

```text
User
  │
  ▼
FastAPI
  │
  ▼
EhSaN Agent
  │
  ├── Conversation Memory
  │
  ├── LLM
  │
  ├── Tool Registry
  │      │
  │      ├── Calculator
  │      ├── Word Counter
  │      ├── DateTime
  │      └── File Reader
  │
  └── Tool Executor
         │
         ▼
      Tool Result
         │
         ▼
      LLM Response
         │
         ▼
       User
```

### Core Components

* **EhSaN Agent** — Main agent interface and orchestration layer.
* **LLM** — Handles communication with the language model.
* **Conversation Memory** — Stores conversation history.
* **Tool Registry** — Registers available tools and their definitions.
* **Tool Executor** — Executes tools requested by the agent.
* **FastAPI** — Provides the REST API.
* **Evaluation** — Measures agent behavior against predefined test cases.
* **Docker** — Provides a reproducible containerized environment.
* **GitHub Actions** — Automatically runs the test suite on pushes and pull requests.

## Project Structure

```text
ai-engineering-agent/
│
├── agent/
│   ├── agent.py
│   ├── llm.py
│   ├── memory.py
│   ├── tool_executor.py
│   ├── tool_registry.py
│   └── tool_selector.py
│
├── tools/
│   ├── calculator.py
│   ├── text_tool.py
│   ├── datetime_tool.py
│   ├── file_reader.py
│   ├── definitions.py
│   └── web_search.py
│
├── evaluation/
│   ├── evaluator.py
│   ├── cases.py
│   ├── mock_agent.py
│   └── run_evaluation.py
│
├── tests/
│   ├── test_agent.py
│   ├── test_api.py
│   └── test_agent_factory.py
│
├── api.py
├── agent_factory.py
├── logger.py
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── README.md
```

### Main Directories

* `agent/` — Core AI Agent logic.
* `tools/` — Custom tools available to the agent.
* `evaluation/` — Agent evaluation framework.
* `tests/` — Automated tests.
* `api.py` — FastAPI application.
* `Dockerfile` — Container configuration.

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/EhSaN-AI13/ai-engineering-agent.git
cd ai-engineering-agent
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

#### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```b
```
