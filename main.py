
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.config.ai_config import ai_client
from app.config.settings import settings
from app.core.database import init_db, get_db
from app.api.v1.api import api_router

# Initialize the FastAPI application
app = FastAPI(
    title=settings.app_name,
    description=settings.app_description,
    version=settings.app_version
)

# Configure CORS (Cross-Origin Resource Sharing) middleware
# This allows the frontend to make requests to this API from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=settings.allowed_methods,
    allow_headers=settings.allowed_headers,
)

# Include API routes
app.include_router(api_router, prefix=settings.api_v1_prefix)

# Initialize the database when the application starts
init_db()

@app.get("/")
def greet(ai: bool = False, db: Session = Depends(get_db)):
    """
    Root endpoint with optional AI integration
    
    Args:
        ai (bool): Optional query parameter. If True, uses AI to generate greeting
        db (Session): Database session dependency
        
    Returns:
        dict: Greeting message from AI or static message
    """
    if ai:
        try:
            resp = ai_client.chat.completions.create(
                model="dolphin-x1-8b",
                messages=[{"role": "user", "content": "Say hello"}],
                temperature=0.2
            )
            return {"message": resp.choices[0].message.content, "source": "AI"}
        except Exception as e:
            return {"message": "Hello! (AI unavailable)", "source": "fallback", "error": str(e)}
    else:
        return {"message": "Hello! Product Tracker API is running.", "source": "static"}