from sqlalchemy import create_engine, text
from problem_service.templates import TEMPLATES
import json

# Database connection
DATABASE_URL = "postgresql://postgres:amol@localhost:5432/codeeditor"
engine = create_engine(DATABASE_URL)

def update_templates():
    with engine.connect() as conn:
        # First, update constraints to be proper JSON arrays
        conn.execute(
            text("UPDATE problems SET constraints = '[]'::jsonb WHERE constraints = '' OR constraints = '[]'")
        )
        
        # Then update templates
        for problem_id, templates in TEMPLATES.items():
            # Convert templates to JSON string
            templates_json = json.dumps(templates)
            
            # Update the templates for this problem
            conn.execute(
                text("UPDATE problems SET templates = :templates WHERE id = :id"),
                {"templates": templates_json, "id": problem_id}
            )
            conn.commit()
            print(f"Updated templates for problem: {problem_id}")

if __name__ == "__main__":
    update_templates() 