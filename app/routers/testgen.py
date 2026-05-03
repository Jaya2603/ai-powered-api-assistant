from fastapi import APIRouter
from pydantic import BaseModel
from app.agent.tools import generate_test_cases

router = APIRouter()


class TestGenRequest(BaseModel):
    endpoint_description: str


class TestGenResponse(BaseModel):
    test_cases: str


@router.post("/generate-tests", response_model=TestGenResponse)
async def gen_tests(req: TestGenRequest):
    """Generate test cases for a given API endpoint description."""
    result = generate_test_cases.invoke(req.endpoint_description)
    return TestGenResponse(test_cases=result)
