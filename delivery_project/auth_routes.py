from fastapi import APIRouter,status, Depends
from database import session, engine
from schemas import SignUpModel,LoginModel
from models import User
from fastapi.exceptions import HTTPException 
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(
    prefix="/auth"
)

session=session(bind=engine)


@auth_router.get("/")
async def signup(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()

    except Exception  as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
    return {"message": "bu auth route signup sahifasi"}


@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email=session.query(User).filter(User.email==user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email already exists")
    
    
    db_username=session.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this username already exists")


    new_user=User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff

    )
    session.add(new_user)
    session.commit()
    data={
        'id':new_user.id,
        'username':new_user.username,
        'email':new_user.email,
        'is_staff':new_user.is_staff,
        'is_active':new_user.is_active

    }

    response_model={
        'success':True,
        'code':201,
        'message':'user is created succesfully',
        'data':data
    }

    return response_model


@auth_router.post('login/', status_code=200)
async def login(user:LoginModel, Authorize:AuthJWT=Depends()): #lofin funskiyasi AuhtJWT obyektini argument sifatida jo'natadi

    db_user=session.query(User).filter(User.username==user.username).first()
    if db_user and check_password_hash(db_user.password, user.password):
        access_token=Authorize.create_access_token(subject=db_user.username)
        refresh_token=Authorize.create_refresh_token(subject=db_user.username)

        token={
            'access':access_token,
            'refresh':refresh_token
        }

        response={
            "success":True,
            "code":200,
            "message":"User successfully login",
            "data":token
        }

        return jsonable_encoder(response)  #responsedagilar dict bo'lib keladi,jsonable_encoder shuni json ko'rinishida to'g'irlab beradi
    
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail='invalid username or password')