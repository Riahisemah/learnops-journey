from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base
from app.api import auth, users, modules, lessons, quiz, progress, admin, ml_predict

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Didacticiel DevOps & MLOps API",
    description="Backend API for DevOps & MLOps learning platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(modules.router)
app.include_router(lessons.router)
app.include_router(quiz.router)
app.include_router(progress.router)
app.include_router(admin.router)
app.include_router(ml_predict.router)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Didacticiel DevOps & MLOps API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "environment": settings.ENVIRONMENT}
