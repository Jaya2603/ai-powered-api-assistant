import httpx
import json
from langchain.tools import tool
from app.rag.retriever import retrieve_context


@tool
def call_api(input: str) -> str:
    """
    Make an HTTP API call. Input must be JSON with keys:
    method, url, headers (optional), body (optional).
    Example: {"method": "GET", "url": "https://api.example.com/users"}
    """
    try:
        params = json.loads(input)
        method = params.get("method", "GET").upper()
        url = params["url"]
        headers = params.get("headers", {})
        body = params.get("body", None)

        with httpx.Client(timeout=15) as client:
            response = client.request(method, url, headers=headers, json=body)
        return json.dumps({
            "status_code": response.status_code,
            "body": (
                response.json()
                if response.headers.get("content-type", "").startswith("application/json")
                else response.text
            ),
        })
    except Exception as e:
        return f"Error calling API: {str(e)}"


@tool
def search_api_docs(query: str) -> str:
    """
    Search internal API documentation to understand endpoints,
    request/response formats, or business rules.
    """
    return retrieve_context(query)


@tool
def generate_test_cases(api_description: str) -> str:
    """
    Generate test cases for a given API endpoint or feature description.
    Returns a structured list of test scenarios.
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.messages import HumanMessage, SystemMessage
    from app.config import settings

    llm = ChatOpenAI(
        model=settings.model_name,
        openai_api_key=settings.openai_api_key,
    )
    context = retrieve_context(api_description)

    messages = [
        SystemMessage(content=(
            "You are an expert QA engineer. Given API documentation context and a description, "
            "generate comprehensive test cases in JSON format covering: happy path, edge cases, "
            "auth failures, invalid inputs, and boundary values."
        )),
        HumanMessage(content=f"Context:\n{context}\n\nAPI to test:\n{api_description}"),
    ]
    response = llm.invoke(messages)
    return response.content
