from fastapi import APIRouter
from database import Session, engine
from schemas import SignUpModel


auth_router = APIRouter(
    prefix="/auth",
)

@auth_router.get("/")
async def signup():
    return {"message": "bu auth route signup sahifasi"}

@auth_router.post("/signup")
async def signup():
    pass