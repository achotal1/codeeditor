from pydantic import BaseModel
from typing import List, Dict, Optional

class Example(BaseModel):
    input: str
    output: str
    explanation: Optional[str] = None

class TestCase(BaseModel):
    id: str
    input: str
    expected_output: str

class Problem(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    acceptance_rate: float
    examples: List[Example]
    constraints: List[str]
    test_cases: List[TestCase]
    templates: Dict[str, str]

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