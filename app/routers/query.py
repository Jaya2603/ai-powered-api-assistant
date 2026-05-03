from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.agent.agent import build_agent, run_agent

router = APIRouter()
_agent = None


def get_agent():
    """Get or initialize the agent singleton."""
    global _agent
    if _agent is None:
        _agent = build_agent()
    return _agent


class QueryRequest(BaseModel):
    query: str
    chat_history: list[dict] = []


class QueryResponse(BaseModel):
    result: str
    steps: list[str] = []


@router.post("/query", response_model=QueryResponse)
async def handle_query(req: QueryRequest):
    """Handle a natural language query using the AI agent."""
    try:
        agent = get_agent()
        result = run_agent(agent, req.query, req.chat_history)
        return QueryResponse(
            result=result["output"],
            steps=result["steps"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
