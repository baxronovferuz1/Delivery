from fastapi import APIRouter,status
from database import session, engine
from schemas import SignUpModel
from models import User
from fastapi.exceptions import HTTPException 


auth_router = APIRouter(
    prefix="/auth",
)

@auth_router.get("/")
async def signup():
    return {"message": "bu auth route signup sahifasi"}


@auth_router.post("/signup")
async def signup(user: SignUpModel):
    db_email=session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists")
    
    
    db_username=session.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this username already exists")
