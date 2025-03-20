from fastapi import FastAPI
from problem_service.router import router as problem_router
from judge_service.router import router as judge_router
app = FastAPI(title="CodeEditor API", description="API for CodeEditor")

# Include routers from different services
app.include_router(problem_router)
app.include_router(judge_router)

@app.get("/")
async def root():
    return {"message": "API is running. Go to /docs for documentation."}

# Run with: uvicorn app.main:app --reload