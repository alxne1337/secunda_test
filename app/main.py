from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database.core import get_db
from app.controllers.buildings import router as building_router
from app.controllers.organizations import router as organizations_router

API_KEY = "12fhg79"
API_KEY_NAME = "API-Key"

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def verify_api_key(api_key: str = Depends(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return api_key

app.include_router(
    organizations_router,
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    building_router,
    dependencies=[Depends(verify_api_key)]
)

@app.get("/")
async def root():
    return {"message": "Organizations API Service"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/test-db")
async def test_db_connection(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT 1"))
        return {"database_status": "connected", "result": result.scalar()}
    except Exception as e:
        return {"database_status": "error", "detail": str(e)}