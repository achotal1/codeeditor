import httpx
import asyncio
import os
from fastapi import HTTPException
from dotenv import load_dotenv

load_dotenv()

JUDGE0_API_URL = os.getenv("JUDGE0_API_URL")
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY")
JUDGE0_API_HOST = os.getenv("JUDGE0_API_HOST")

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

async def send_to_judge0(code: str, language_id: int, stdin: str = ""):
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
        "cpu_time_limit": 2,  # 2 seconds
        "memory_limit": 512000,  # 512 MB
        "expected_output": None,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            # Create submission
            response = await client.post(
                f"{JUDGE0_API_URL}/submissions", 
                json=payload, 
                headers=headers
            )
            
            if response.status_code != 201:
                raise HTTPException(status_code=500, detail="Failed to create submission")
            
            submission_token = response.json()["token"]
            
            # Wait for result (with timeout)
            max_attempts = 10
            for _ in range(max_attempts):
                await asyncio.sleep(1)
                
                result_response = await client.get(
                    f"{JUDGE0_API_URL}/submissions/{submission_token}",
                    headers=headers
                )
                
                if result_response.status_code != 200:
                    raise HTTPException(status_code=500, detail="Failed to get submission result")
                
                result = result_response.json()
                
                # Check if processing is complete
                if result["status"]["id"] not in [1, 2]:  # 1: In Queue, 2: Processing
                    return result
            
            raise HTTPException(status_code=408, detail="Execution timed out")
            
        except httpx.RequestError as exc:
            raise HTTPException(status_code=503, detail=f"Judge0 service error: {str(exc)}")