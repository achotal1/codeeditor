import requests
import json
from typing import Dict, List, Tuple, Any
from sqlalchemy.orm import Session
from problem_service.model import ProblemCreate, TestCaseCreate, create_problem
from problem_service.database import SessionLocal

def fetch_problem(title_slug: str) -> Dict[str, Any]:
    """Fetch problem data from LeetCode GraphQL API."""
    query = """
    query questionData($titleSlug: String!) {
        question(titleSlug: $titleSlug) {
            questionId
            title
            titleSlug
            content
            difficulty
            stats
            topicTags {
                name
            }
            codeSnippets {
                lang
                code
            }
            exampleTestcases
            sampleTestCase
        }
    }
    """
    
    url = "https://leetcode.com/graphql"
    response = requests.post(url, json={
        "query": query,
        "variables": {"titleSlug": title_slug}
    })
    
    if response.status_code == 200:
        return response.json()["data"]["question"]
    else:
        raise Exception(f"Failed to fetch problem: {response.status_code}")

def parse_problem_data(data: Dict[str, Any]) -> Tuple[ProblemCreate, List[TestCaseCreate]]:
    """Parse raw problem data into ProblemCreate and TestCaseCreate objects."""
    # Parse stats JSON string to get acceptance rate
    stats = json.loads(data["stats"])
    acceptance_rate = float(stats["acRate"].strip("%")) / 100
    
    # Get topics
    topics = [tag["name"] for tag in data["topicTags"]]
    
    # Parse code templates
    templates = {
        snippet["lang"]: snippet["code"]
        for snippet in data["codeSnippets"]
    }
    
    # Create problem
    problem = ProblemCreate(
        id=data["titleSlug"],
        title=data["title"],
        description=data["content"],
        difficulty=data["difficulty"],
        acceptance_rate=acceptance_rate,
        topics=topics,
        templates=templates,
        examples=[],  # We'll parse these from the content
        constraints=""  # We'll parse these from the content
    )
    
    # Create test cases
    test_cases = []
    if data["sampleTestCase"]:
        lines = data["sampleTestCase"].strip().split("\n")
        for i, line in enumerate(lines):
            test_case = TestCaseCreate(
                id=f"{problem.id}-{i+1}",
                problem_id=problem.id,
                input=line,
                expected_output=""  # We need to figure out how to get expected outputs
            )
            test_cases.append(test_case)
    
    return problem, test_cases

def fetch_and_save_problem(db: Session, title_slug: str) -> None:
    """Fetch a problem from LeetCode and save it to the database."""
    try:
        # Fetch problem data
        data = fetch_problem(title_slug)
        
        # Parse data
        problem, test_cases = parse_problem_data(data)
        
        # Save to database
        create_problem(db, problem, test_cases)
        print(f"Successfully updated problem: {problem.title}")
        
    except Exception as e:
        print(f"Error processing problem {title_slug}: {str(e)}")

def main():
    """Fetch and save popular LeetCode problems."""
    popular_problems = [
        "two-sum",
        "add-two-numbers",
        "longest-substring-without-repeating-characters",
        "median-of-two-sorted-arrays",
        "longest-palindromic-substring",
        "zigzag-conversion",
        "reverse-integer",
        "string-to-integer-atoi",
        "palindrome-number",
        "regular-expression-matching"
    ]
    
    db = SessionLocal()
    try:
        for title_slug in popular_problems:
            fetch_and_save_problem(db, title_slug)
    finally:
        db.close()

if __name__ == "__main__":
    main() 