from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class SubmissionCreate(BaseModel):
    problem_id: str
    language: str
    code: str
    test_case_id: Optional[str] = None

class SubmissionResult(BaseModel):
    status: str
    stdout: Optional[str] = None
    stderr: Optional[str] = None
    execution_time: float
    memory_used: int

class TestCaseResult(BaseModel):
    test_case_id: str
    status: str
    execution_time: float
    memory_used: int
    stdout: Optional[str] = None
    stderr: Optional[str] = None

class SubmissionResponse(BaseModel):
    id: str
    problem_id: str
    language: str
    status: str
    execution_time: float
    memory_used: int
    passed_count: int
    total_count: int
    results: List[TestCaseResult]

# Language IDs for Judge0
LANGUAGE_IDS = {
    "python": 71,
    "javascript": 63,
    "java": 62,
    "cpp": 54,
    "c": 50,
    "rust": 73,
    "go": 60,
    "ruby": 72,
    "swift": 83,
    "kotlin": 78,
    "scala": 81,
    "php": 68,
    "typescript": 74,
    "r": 80,
    "bash": 46,
    "sql": 82,
    "pascal": 67,
    "csharp": 51,
    "dart": 55,
    "elixir": 57,
    "erlang": 58,
    "fsharp": 59,
    "haskell": 61,
    "lua": 64,
    "ocaml": 65,
    "perl": 66,
    "racket": 79,
    "scheme": 77,
    "text": 45,
    "plaintext": 45,
    "vbnet": 84,
    "clojure": 86,
    "groovy": 87,
    "julia": 88,
    "lolcode": 89,
    "brainfuck": 90,
    "fortran": 91,
    "octave": 92,
    "cobol": 93,
    "icon": 94,
    "idris": 95,
    "nim": 96,
    "pike": 97,
    "smalltalk": 98,
    "whitespace": 99,
    "tsql": 100,
    "tcl": 101,
    "objectivec": 102,
    "coffeescript": 103,
    "lisp": 104,
    "d": 105,
    "prolog": 106,
    "fantom": 107,
    "factor": 108,
    "falcon": 109,
    "fancy": 110,
    "forth": 111,
    "io": 112,
    "j": 113,
    "jade": 114,
    "java8": 115,
    "moon": 116,
    "nemerle": 117,
    "nice": 118,
    "nodejs": 119,
    "oz": 120,
    "pogoscript": 121,
    "yabasic": 122,
    "zsh": 123,
    "ada": 124,
    "algol": 125
}

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
    code: Optional[str] = None

class SubmissionHistory(BaseModel):
    id: str
    language: str
    status: str
    created_at: str
    execution_time: float
    memory_used: float
    passed_count: int
    total_count: int