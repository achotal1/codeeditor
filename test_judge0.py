import httpx
import asyncio
import os
from dotenv import load_dotenv
import json

load_dotenv()

JUDGE0_API_URL = os.getenv("JUDGE0_API_URL")
JUDGE0_API_KEY = os.getenv("JUDGE0_API_KEY")
JUDGE0_API_HOST = os.getenv("JUDGE0_API_HOST")

async def test_judge0():
    headers = {
        "Content-Type": "application/json",
        "X-RapidAPI-Key": JUDGE0_API_KEY,
        "X-RapidAPI-Host": JUDGE0_API_HOST,
    }
    
    payload = {
        "language_id": 71,  # Python
        "source_code": "print('Hello, World!')",
        "stdin": "",
        "expected_output": "Hello, World!\n",
        "cpu_time_limit": 2,
        "memory_limit": 512000,
    }
    
    print("Making request to Judge0 API...")
    print(f"URL: {JUDGE0_API_URL}")
    print(f"Headers: {json.dumps(headers, indent=2)}")
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    async with httpx.AsyncClient() as client:
        try:
            # Create submission
            response = await client.post(
                f"{JUDGE0_API_URL}/submissions", 
                json=payload, 
                headers=headers
            )
            
            print(f"\nCreate submission response:")
            print(f"Status code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code != 201:
                print("Failed to create submission")
                return
            
            submission_token = response.json()["token"]
            print(f"\nGot submission token: {submission_token}")
            
            # Wait for result
            max_attempts = 10
            for attempt in range(max_attempts):
                await asyncio.sleep(1)
                print(f"\nChecking submission status (attempt {attempt + 1}/{max_attempts})")
                
                result_response = await client.get(
                    f"{JUDGE0_API_URL}/submissions/{submission_token}",
                    headers=headers
                )
                
                print(f"Status code: {result_response.status_code}")
                print(f"Response: {result_response.text}")
                
                if result_response.status_code != 200:
                    print("Failed to get submission result")
                    return
                
                result = result_response.json()
                
                # Check if processing is complete
                if result["status"]["id"] not in [1, 2]:  # 1: In Queue, 2: Processing
                    print("\nProcessing complete!")
                    print(f"Final result: {json.dumps(result, indent=2)}")
                    return
            
            print("\nExecution timed out")
            
        except Exception as e:
            print(f"\nError: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_judge0()) 