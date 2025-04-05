from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, task
from app.core.config import settings

app = FastAPI(
    title="FastAPI Auth Example",
    description="A FastAPI application with JWT authentication",
    version="1.0.0"
)

# Configure CORS
origins = settings.CORS_ORIGINS.split(",") if hasattr(settings, "CORS_ORIGINS") else ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(task.router)

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI with JWT Authentication!"} 