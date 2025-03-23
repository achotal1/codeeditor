from fastapi import APIRouter, HTTPException
from .model import (
    RunSubmissionRequest, 
    SubmitSolutionRequest, 
    SubmissionResponse, 
    TestResult,
    LANGUAGE_IDS
)
from .judge0_client import send_to_judge0, STATUS_MAP
from problem_service.model import problems
import uuid

router = APIRouter(
    prefix="/api/submissions",
    tags=["submissions"],
    responses={404: {"description": "Not found"}},
)

# In-memory submission storage (replace with a database in production)
submissions = {}

@router.post("/run", response_model=SubmissionResponse)
async def run_submission(request: RunSubmissionRequest):
    """Run code against a single test case."""
    # Find problem
    problem = next((p for p in problems if p["id"] == request.problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Find test case
    test_case = next((tc for tc in problem["test_cases"] if tc["id"] == request.test_case_id), None)
    if not test_case:
        raise HTTPException(status_code=404, detail="Test case not found")
    
    # Get language ID
    language_id = LANGUAGE_IDS.get(request.language)
    if not language_id:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    # Send to Judge0
    try:
        result = await send_to_judge0(request.code, language_id, test_case["input"])
        
        # Get status
        status = STATUS_MAP.get(result["status"]["id"], "Unknown")
        
        # Prepare response
        submission_id = str(uuid.uuid4())
        response = SubmissionResponse(
            id=submission_id,
            status=status,
            output=result.get("stdout", ""),
            execution_time=result.get("time", 0),
            memory_used=result.get("memory", 0),
            stderr=result.get("stderr", ""),
            expected_output=test_case["expected_output"]
        )
        
        # Save submission to memory
        submissions[submission_id] = {
            "id": submission_id,
            "problem_id": request.problem_id,
            "language": request.language,
            "code": request.code,
            "status": status,
            "created_at": str(uuid.uuid1()),
            "execution_time": result.get("time", 0),
            "memory_used": result.get("memory", 0),
        }
        
        return response
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/submit", response_model=SubmissionResponse)
async def submit_solution(request: SubmitSolutionRequest):
    """Submit solution to run against all test cases."""
    # Find problem
    problem = next((p for p in problems if p["id"] == request.problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")
    
    # Get language ID
    language_id = LANGUAGE_IDS.get(request.language)
    if not language_id:
        raise HTTPException(status_code=400, detail="Unsupported language")
    
    # Run against each test case
    test_results = []
    passed_count = 0
    total_time = 0
    max_memory = 0
    
    for test_case in problem["test_cases"]:
        try:
            result = await send_to_judge0(request.code, language_id, test_case["input"])
            
            output = result.get("stdout", "").strip()
            expected_output = test_case["expected_output"].strip()
            passed = (output == expected_output) and (result["status"]["id"] == 3)  # 3 = Accepted
            
            if passed:
                passed_count += 1
            
            test_results.append(TestResult(
                input=test_case["input"],
                output=output,
                expected_output=expected_output,
                passed=passed
            ))
            
            # Track resource usage
            total_time += result.get("time", 0)
            max_memory = max(max_memory, result.get("memory", 0))
            
        except Exception as e:
            test_results.append(TestResult(
                input=test_case["input"],
                output=str(e),
                expected_output=test_case["expected_output"],
                passed=False
            ))
    
    # Determine overall status
    status = "Accepted" if passed_count == len(problem["test_cases"]) else "Wrong Answer"
    
    # Save submission
    submission_id = str(uuid.uuid4())
    submissions[submission_id] = {
        "id": submission_id,
        "problem_id": request.problem_id,
        "language": request.language,
        "code": request.code,
        "status": status,
        "created_at": str(uuid.uuid1()),
        "passed_count": passed_count,
        "total_count": len(problem["test_cases"]),
        "execution_time": total_time / len(problem["test_cases"]) if len(problem["test_cases"]) > 0 else 0,
        "memory_used": max_memory,
    }
    
    # Prepare response
    avg_time = total_time / len(problem["test_cases"]) if len(problem["test_cases"]) > 0 else 0
    return SubmissionResponse(
        id=submission_id,
        status=status,
        test_results=test_results,
        execution_time=avg_time,
        memory_used=max_memory,
        passed=passed_count,
        total=len(problem["test_cases"])
    )