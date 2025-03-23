from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from problem_service.router import router as problem_router
from judge_service.router import router as judge_router
app = FastAPI(title="CodeEditor API", description="API for CodeEditor")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL of your frontend
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Include routers from different services
app.include_router(problem_router)
app.include_router(judge_router)

@app.get("/")
async def root():
    return {"message": "API is running. Go to /docs for documentation."}

# Run with: uvicorn app.main:app --reload