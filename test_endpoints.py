import requests
import json

BASE_URL = "http://localhost:8000"

def test_run():
    print("\nTesting run endpoint...")
    payload = {
        "problem_id": "two-sum",
        "language": "python",
        "code": """
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

# Parse input
def parse_input():
    nums = list(map(int, input().strip('[]').split(',')))
    target = int(input())
    return nums, target

if __name__ == "__main__":
    nums, target = parse_input()
    solution = Solution()
    result = solution.twoSum(nums, target)
    print(result)
""",
        "test_case_id": "two-sum-1"
    }
    
    print("Sending payload:", json.dumps(payload, indent=2))
    try:
        response = requests.post(f"{BASE_URL}/api/submissions/run", json=payload)
        print(f"Status Code: {response.status_code}")
        try:
            print("Response:", json.dumps(response.json(), indent=2))
        except:
            print("Raw Response:", response.text)
            print("Response Headers:", dict(response.headers))
    except Exception as e:
        print("Error:", str(e))

def test_submission():
    print("\nTesting submission endpoint...")
    payload = {
        "problem_id": "two-sum",
        "language": "python",
        "code": """
class Solution:
    def twoSum(self, nums, target):
        seen = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in seen:
                return [seen[complement], i]
            seen[num] = i
        return []

# Parse input
def parse_input():
    nums = list(map(int, input().strip('[]').split(',')))
    target = int(input())
    return nums, target

if __name__ == "__main__":
    nums, target = parse_input()
    solution = Solution()
    result = solution.twoSum(nums, target)
    print(result)
"""
    }
    
    print("Sending payload:", json.dumps(payload, indent=2))
    try:
        response = requests.post(f"{BASE_URL}/api/submissions/submit", json=payload)
        print(f"Status Code: {response.status_code}")
        try:
            print("Response:", json.dumps(response.json(), indent=2))
        except:
            print("Raw Response:", response.text)
            print("Response Headers:", dict(response.headers))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    test_run()
    test_submission() 