from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from app.agent.tools import call_api, search_api_docs, generate_test_cases
from app.config import settings


SYSTEM_PROMPT = (
    "You are an expert API assistant. You help users interact with APIs "
    "using natural language. You can search API documentation, make HTTP calls, "
    "and generate test cases. Always search docs before making API calls to understand "
    "the correct endpoint format and authentication requirements."
)


def build_agent():
    """Build and return the LangChain agent using the modern create_agent API."""
    llm = ChatOpenAI(
        model=settings.model_name,
        openai_api_key=settings.openai_api_key,
        temperature=0,
    )

    tools = [call_api, search_api_docs, generate_test_cases]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
    )
    return agent


def run_agent(agent, query: str, chat_history: list[dict] | None = None) -> dict:
    """
    Run the agent with a query and optional chat history.

    Returns a dict with 'output' (the final response) and 'messages' (full message list).
    """
    # Build the messages list from chat history + current query
    messages = []
    if chat_history:
        for msg in chat_history:
            role = msg.get("role", "human")
            content = msg.get("content", "")
            if role in ("human", "user"):
                messages.append(HumanMessage(content=content))
            else:
                from langchain_core.messages import AIMessage
                messages.append(AIMessage(content=content))

    messages.append(HumanMessage(content=query))

    # Invoke the agent
    result = agent.invoke({"messages": messages})

    # Extract the final AI response
    output_messages = result.get("messages", [])
    final_output = ""
    steps = []

    for msg in output_messages:
        if hasattr(msg, "type"):
            if msg.type == "ai" and msg.content and not getattr(msg, "tool_calls", None):
                final_output = msg.content
            elif msg.type == "tool":
                steps.append(f"Tool({msg.name}): {msg.content[:200]}")

    return {
        "output": final_output,
        "steps": steps,
        "messages": output_messages,
    }
