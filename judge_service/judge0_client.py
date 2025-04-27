import httpx
import asyncio
import os
from fastapi import HTTPException
from dotenv import load_dotenv
from .model import SubmissionResult
import logging

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

JUDGE0_API_URL = os.getenv("JUDGE0_API_URL")
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY")
JUDGE0_API_HOST = os.getenv("JUDGE0_API_HOST")

# Language mapping
LANGUAGE_MAP = {
    "python": 71,  # Python (3.8.1)
    "cpp": 54,    # C++ (GCC 9.2.0)
}

# Status code mapping
STATUS_MAP = {
    3: "Accepted",
    4: "Wrong Answer",
    5: "Time Limit Exceeded",
    6: "Compilation Error",
    7: "Runtime Error (SIGSEGV)",
    8: "Runtime Error (SIGXFSZ)",
    9: "Runtime Error (SIGFPE)",
    10: "Runtime Error (SIGABRT)",
    11: "Runtime Error (NZEC)",
    12: "Runtime Error (Other)",
    13: "Internal Error",
    14: "Exec Format Error",
}

async def send_to_judge0(code: str, language_id: int, stdin: str = "", expected_output: str = None):
    """Send code to Judge0 API for execution."""
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": JUDGE0_API_KEY,
        "X-RapidAPI-Host": JUDGE0_API_HOST,
    }
    
    payload = {
        "language_id": language_id,
        "source_code": code,
        "stdin": stdin,
        "expected_output": expected_output,
        "cpu_time_limit": 2,  # 2 seconds
        "memory_limit": 512000,  # 512 MB
    }
    
    logger.debug(f"Sending request to Judge0 API: {JUDGE0_API_URL}")
    logger.debug(f"Headers: {headers}")
    logger.debug(f"Payload: {payload}")
    
    async with httpx.AsyncClient() as client:
        try:
            # Create submission
            response = await client.post(
                f"{JUDGE0_API_URL}/submissions", 
                json=payload, 
                headers=headers
            )
            
            logger.debug(f"Create submission response: {response.status_code}")
            logger.debug(f"Response content: {response.text}")
            
            if response.status_code != 201:
                logger.error(f"Failed to create submission: {response.text}")
                raise HTTPException(status_code=500, detail=f"Failed to create submission: {response.text}")
            
            submission_token = response.json()["token"]
            logger.debug(f"Got submission token: {submission_token}")
            
            # Wait for result (with timeout)
            max_attempts = 10
            for attempt in range(max_attempts):
                await asyncio.sleep(1)
                logger.debug(f"Checking submission status (attempt {attempt + 1}/{max_attempts})")
                
                result_response = await client.get(
                    f"{JUDGE0_API_URL}/submissions/{submission_token}",
                    headers=headers
                )
                
                logger.debug(f"Get result response: {result_response.status_code}")
                logger.debug(f"Response content: {result_response.text}")
                
                if result_response.status_code != 200:
                    logger.error(f"Failed to get submission result: {result_response.text}")
                    raise HTTPException(status_code=500, detail=f"Failed to get submission result: {result_response.text}")
                
                result = result_response.json()
                
                # Check if processing is complete
                if result["status"]["id"] not in [1, 2]:  # 1: In Queue, 2: Processing
                    logger.debug(f"Processing complete. Result: {result}")
                    return result
            
            logger.error("Execution timed out")
            raise HTTPException(status_code=408, detail="Execution timed out")
            
        except httpx.RequestError as e:
            logger.error(f"HTTP request failed: {str(e)}")
            raise HTTPException(status_code=500, detail=f"HTTP request failed: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

async def execute_code(code: str, language: str, stdin: str = "", expected_output: str = None) -> SubmissionResult:
    """Execute code using Judge0 and return results."""
    if language not in LANGUAGE_MAP:
        logger.error(f"Unsupported language: {language}")
        raise HTTPException(status_code=400, detail=f"Unsupported language: {language}")
    
    language_id = LANGUAGE_MAP[language]
    logger.debug(f"Executing code for language {language} (ID: {language_id})")
    
    try:
        result = await send_to_judge0(code, language_id, stdin, expected_output)
        
        # Check for compilation errors
        if result.get("compile_output"):
            return SubmissionResult(
                status="Compilation Error",
                stdout="",
                stderr=result["compile_output"],
                execution_time=0.0,
                memory_used=0
            )
        
        # Check for runtime errors
        if result.get("stderr"):
            return SubmissionResult(
                status="Runtime Error",
                stdout=result.get("stdout", ""),
                stderr=result["stderr"],
                execution_time=float(result.get("time", 0)),
                memory_used=int(result.get("memory", 0))
            )
        
        # Check if output matches expected output
        if expected_output and result.get("stdout") != expected_output:
            return SubmissionResult(
                status="Wrong Answer",
                stdout=result.get("stdout", ""),
                stderr="",
                execution_time=float(result.get("time", 0)),
                memory_used=int(result.get("memory", 0))
            )
        
        # Success case
        return SubmissionResult(
            status=STATUS_MAP.get(result["status"]["id"], "Unknown"),
            stdout=result.get("stdout", ""),
            stderr=result.get("stderr", ""),
            execution_time=float(result.get("time", 0)),
            memory_used=int(result.get("memory", 0))
        )
    except Exception as e:
        logger.error(f"Error executing code: {str(e)}")
        raise