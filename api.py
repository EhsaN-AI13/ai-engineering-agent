from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import BaseModel, Field
from contextlib import asynccontextmanager

from agent_factory import create_agent

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.agent = create_agent()

    yield

    app.state.agent = None

app = FastAPI(
    title="EhsaN AI Agent",
    lifespan=lifespan
)

def get_agent():
    return app.state.agent


app.state.agent = create_agent()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1)


@app.get("/")
def root():
    return {
        "message": "EhsaN AI Agent API is running."
    }

class ChatResponse(BaseModel):
    response: str

@app.post("/chat", response_model=ChatResponse)
def chat(
    request: ChatRequest,
    agent=Depends(get_agent)
):
    try:
        response = agent.run(request.message)

        return {
            "response": response
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred."
        )