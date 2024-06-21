from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from models import User,Product,Order
from schemas import OrderModel,OrderStatusModel
from database import session,engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

order_router = APIRouter(
    prefix="/order",
)



@order_router.get("/")
async def welcome_page(Authorize: AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")  

    return {
        "message":"Bu order route sahifasi"
    }  


@order_router.post('/make', status_code=status.HTTP_201_CREATED)
async def make_order(order:OrderModel, Authorize:AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Enter valid access token")
    
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        quantity=order.quantity,
        #product=order.product_id
    )
    new_order.user=user
    session.add(new_order)
    session.commit()

    response={
        "id":new_order.id,
        "quantity":new_order.quantity,
        "order_statuses":new_order.order_status,
    }

    return jsonable_encoder(response)