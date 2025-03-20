# FastAPI Sample Project

A simple REST API built with FastAPI.

## Setup and Installation

### Prerequisites
- Python 3.7+
- Virtual environment (venv)

### Installation Steps

1. **Activate the virtual environment**

   On Windows:
   ```
   venv\Scripts\activate
   ```

   On macOS/Linux:
   ```
   source venv/bin/activate
   ```

2. **Install dependencies**
   ```
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```
   uvicorn main:app --reload
   ```
   
   Or use Python directly:
   ```
   python main.py
   ```

4. **Access the API**
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc
   - API root: http://localhost:8000/

## Key Python Concepts (Coming from TypeScript)

### 1. Virtual Environment vs node_modules
- `venv` is a self-contained Python environment with its own interpreter and packages
- Similar to `node_modules` but more isolated from the system

### 2. Type Hints
- Optional in Python (vs. mandatory in TypeScript)
- Used for documentation, IDE support, and static type checking
- Not enforced at runtime

### 3. Package Management
- `requirements.txt` is similar to `package.json` but simpler
- `pip` is the package manager (similar to npm/yarn)

### 4. FastAPI Features
- Automatic OpenAPI documentation
- Request validation using Pydantic models
- Dependency injection system
- High performance (based on Starlette and Pydantic)

## API Endpoints

- `GET /`: Welcome message
- `GET /items/`: List all items
- `GET /items/{item_id}`: Get a specific item
- `POST /items/`: Create a new item
- `GET /items/search/?q=query`: Search items by name or description 