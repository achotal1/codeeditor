from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from sqlalchemy.orm import Session
from problem_service import db_models
from .database import get_db
import uuid

# Pydantic models for request/response
class ExampleBase(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None

class ExampleCreate(ExampleBase):
    pass

class Example(ExampleBase):
    id: int
    problem_id: str

    class Config:
        from_attributes = True

class TestCaseBase(BaseModel):
    input: str
    expected_output: str
    is_hidden: bool = False
    time_limit: Optional[int] = None  # in milliseconds
    memory_limit: Optional[int] = None  # in MB
    order: int

class TestCaseCreate(BaseModel):
    id: str
    problem_id: str
    input: str
    expected_output: str

class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: str
    acceptance_rate: float
    constraints: List[str]
    templates: Dict[str, str]
    topics: List[str]
    has_examples: bool = True

class ProblemCreate(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    acceptance_rate: float
    topics: Optional[List[str]] = None
    examples: Optional[List[Dict[str, Any]]] = None
    constraints: Optional[str] = None
    templates: Optional[Dict[str, str]] = None

class Problem(ProblemBase):
    id: str
    test_cases: List[TestCaseCreate]
    premium: bool = False
    likes: int = 0
    dislikes: int = 0
    frequency: float = 0.0

    class Config:
        from_attributes = True

# Database operations
def get_problem(db: Session, problem_id: str):
    return db.query(db_models.Problem).filter(db_models.Problem.id == problem_id).first()

def get_problems(db: Session, skip: int = 0, limit: int = 100):
    return db.query(db_models.Problem).offset(skip).limit(limit).all()

def create_problem(db: Session, problem: ProblemCreate, test_cases: List[TestCaseCreate]):
    db_problem = db_models.Problem(
        id=problem.id,
        title=problem.title,
        description=problem.description,
        difficulty=problem.difficulty,
        acceptance_rate=problem.acceptance_rate,
        topics=problem.topics,
        examples=problem.examples,
        constraints=problem.constraints,
        templates=problem.templates
    )
    db.add(db_problem)
    db.commit()
    db.refresh(db_problem)

    for test_case in test_cases:
        db_test_case = db_models.TestCase(
            id=test_case.id,
            problem_id=test_case.problem_id,
            input=test_case.input,
            expected_output=test_case.expected_output
        )
        db.add(db_test_case)
    
    db.commit()
    return db_problem

# Sample problem data (in-memory database for now)
problems = [
    {
        "id": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "acceptance_rate": 86.5,
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target.",
        "examples": [
            {
                "input": "nums = [2,7,11,15], target = 9",
                "output": "[0,1]",
                "explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."
            }
        ],
        "constraints": [
              "2 <= nums.length <= 10^4",
             "-10^9 <= nums[i] <= 10^9"
            ],
        "test_cases": [
            {
               "id": "two-sum-1",
              "input": "2 7 11 15\n9",
              "expected_output": "[0,1]"
           }
        ],
        "templates": {
            "python": "def two_sum(nums, target):\n    pass"
        }
    }
]