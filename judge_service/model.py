from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# Language IDs for Judge0
LANGUAGE_IDS = {
    "python": 71,     # Python 3.8
    "javascript": 63, # JavaScript Node.js
    "java": 62,       # Java 13
    "cpp": 54,        # C++ GCC 9.2
}

# Request models
class RunSubmissionRequest(BaseModel):
    problem_id: str
    language: str
    code: str
    test_case_id: str

class SubmitSolutionRequest(BaseModel):
    problem_id: str
    language: str
    code: str

# Response models
class TestResult(BaseModel):
    input: str
    output: str
    expected_output: str
    passed: bool

class SubmissionResponse(BaseModel):
    id: Optional[str] = None
    status: str
    output: Optional[str] = None
    execution_time: Optional[float] = None
    stderr: Optional[str] = None
    memory_used: Optional[float] = None
    test_results: Optional[List[TestResult]] = None
    passed: Optional[int] = None
    total: Optional[int] = None
    expected_output: Optional[str] = None