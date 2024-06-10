from fastapi import APIRouter


auth_router = APIRouter(
    prefix="/auth",
)

@auth_router.get("/")
async def signup():
    return {"message": "bu auth route signup sahifasi"}