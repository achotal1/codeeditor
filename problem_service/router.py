from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session

from .model import Problem, ProblemCreate, get_problem, get_problems, create_problem
from .database import get_db

router = APIRouter(
    prefix="/api/problems",
    tags=["problems"],
    responses={404: {"description": "Problem not found"}},
)

@router.get("/", response_model=List[Problem])
async def get_problems_list(db: Session = Depends(get_db)):
    """Get a list of all problems."""
    return get_problems(db)

@router.get("/{problem_id}", response_model=Problem)
async def get_problem_by_id(problem_id: str, db: Session = Depends(get_db)):
    """Get details of a specific problem."""
    problem = get_problem(db, problem_id)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    return problem

@router.post("/", response_model=Problem)
async def create_new_problem(problem: ProblemCreate, db: Session = Depends(get_db)):
    """Create a new problem."""
    return create_problem(db, problem) 