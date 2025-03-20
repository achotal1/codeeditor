from fastapi import APIRouter, HTTPException
from typing import List

from .model import problems

router = APIRouter(
    prefix="/api/problems",
    tags=["problems"],
    responses={404: {"description": "Problem not found"}},
)

@router.get("/", response_model=List[dict])
async def get_problems():
    """Get a list of all problems."""
    return [
        {
            "id": problem["id"],
            "title": problem["title"],
            "difficulty": problem["difficulty"],
            "acceptance_rate": problem["acceptance_rate"]
        }
        for problem in problems
    ]

@router.get("/{problem_id}", response_model=dict)
async def get_problem(problem_id: str):
    """Get details of a specific problem."""
    problem = next((p for p in problems if p["id"] == problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem 