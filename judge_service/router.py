from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, judge0_client
from .database import get_db
from .model import SubmissionCreate, SubmissionResponse, SubmissionResult, TestCaseResult
from problem_service import db_models as problem_models
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/submissions", tags=["submissions"])

@router.post("/run", response_model=SubmissionResult)
async def run_submission(
    submission: SubmissionCreate,
    db: Session = Depends(get_db)
):
    """
    Run code against a single test case
    """
    # Get the problem and test case
    problem = db.query(problem_models.Problem).filter(problem_models.Problem.id == submission.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    test_case = db.query(problem_models.TestCase).filter(problem_models.TestCase.id == submission.test_case_id).first()
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    
    # Create submission record
    db_submission = models.Submission(
        id=str(uuid.uuid4()),
        problem_id=submission.problem_id,
        language=submission.language,
        code=submission.code,
        status="Running"
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    try:
        # Execute code using Judge0
        result = await judge0_client.execute_code(
            code=submission.code,
            language=submission.language,
            stdin=test_case.input,
            expected_output=test_case.expected_output
        )
        
        # Update submission status
        db_submission.status = result.status
        db_submission.execution_time = result.execution_time
        db_submission.memory_used = result.memory_used
        db_submission.stdout = result.stdout
        db_submission.stderr = result.stderr
        db.commit()
        
        return result
        
    except Exception as e:
        db_submission.status = "Error"
        db_submission.stderr = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit", response_model=SubmissionResponse)
async def submit_solution(
    submission: SubmissionCreate,
    db: Session = Depends(get_db)
):
    """
    Submit code for evaluation against all test cases
    """
    # Get the problem and its test cases
    problem = db.query(problem_models.Problem).filter(problem_models.Problem.id == submission.problem_id).first()
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    test_cases = db.query(problem_models.TestCase).filter(problem_models.TestCase.problem_id == submission.problem_id).all()
    if not test_cases:
        raise HTTPException(status_code=404, detail="No test cases found for this problem")
    
    # Create submission record
    db_submission = models.Submission(
        id=str(uuid.uuid4()),
        problem_id=submission.problem_id,
        language=submission.language,
        code=submission.code,
        status="Running"
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    
    results = []
    passed_count = 0
    
    try:
        # Execute code against each test case
        for test_case in test_cases:
            result = await judge0_client.execute_code(
                code=submission.code,
                language=submission.language,
                stdin=test_case.input,
                expected_output=test_case.expected_output
            )
            
            if result.status == "Accepted":
                passed_count += 1
                
            results.append(TestCaseResult(
                test_case_id=test_case.id,
                status=result.status,
                execution_time=result.execution_time,
                memory_used=result.memory_used,
                stdout=result.stdout,
                stderr=result.stderr
            ))
        
        # Update submission status
        db_submission.status = "Accepted" if passed_count == len(test_cases) else "Wrong Answer"
        db_submission.execution_time = max(r.execution_time for r in results)
        db_submission.memory_used = max(r.memory_used for r in results)
        db_submission.passed_count = passed_count
        db_submission.total_count = len(test_cases)
        db.commit()
        
        return SubmissionResponse(
            id=db_submission.id,
            problem_id=db_submission.problem_id,
            language=db_submission.language,
            status=db_submission.status,
            execution_time=db_submission.execution_time,
            memory_used=db_submission.memory_used,
            passed_count=db_submission.passed_count,
            total_count=db_submission.total_count,
            results=results
        )
        
    except Exception as e:
        db_submission.status = "Error"
        db_submission.stderr = str(e)
        db.commit()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: str,
    db: Session = Depends(get_db)
):
    """
    Get details of a specific submission
    """
    submission = db.query(models.Submission).filter(models.Submission.id == submission_id).first()
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Get test case results
    results = []
    test_cases = db.query(problem_models.TestCase).filter(problem_models.TestCase.problem_id == submission.problem_id).all()
    
    for test_case in test_cases:
        results.append(TestCaseResult(
            test_case_id=test_case.id,
            status=submission.status,
            execution_time=submission.execution_time,
            memory_used=submission.memory_used,
            stdout=submission.stdout,
            stderr=submission.stderr
        ))
    
    return SubmissionResponse(
        id=submission.id,
        problem_id=submission.problem_id,
        language=submission.language,
        status=submission.status,
        execution_time=submission.execution_time,
        memory_used=submission.memory_used,
        passed_count=submission.passed_count,
        total_count=submission.total_count,
        results=results
    )