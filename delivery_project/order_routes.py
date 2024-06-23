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

session=session(bind=engine)


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
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail="Enter valid access token")
    
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()

    new_order=Order(
        quantity=order.quantity,
        #product=order.product_id
    )
    new_order.user=user
    session.add(new_order)
    session.commit()
    data={
        "success":True,
        "code":201,
        "message":"new order succesfully created",
        "data":{
            "id":new_order.id,
            "quantity":new_order.quantity,
            "order_statuses":new_order.order_status,
    }
    }

    response=data

    return jsonable_encoder(response)


@order_router.get("/list", status_code=status.HTTP_201_CREATED)
async def order_list(Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized,enter valid access token")
    
    current_user=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==current_user).first()


    if user.is_staff():
        orders=session.query(Order).all()
        data=[
            {
                "id":order.id,
                "user":{
                    "id":order.user.id,
                    "username":order.user.username,
                    "email":order.user.email
                },
                "product_id":order.product_id,
                "quantity":order.quantity,
                "order_statuses":order.order_status.value,
            }
            for order in orders
        ]
        return jsonable_encoder(orders)
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only superadmin can see all orders") #The user is authorized, but does not have permission



@order_router.get("/{id}")
async def order_by_id(id:int , Authorize:AuthJWT=Depends()):


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized,enter valid access token")
    
    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()
        custom_order={
                "id":order.id,
                "user":{
                    "id":order.user.id,
                    "username":order.user.username,
                    "email":order.user.email
                },
                "product_id":order.product_id,
                "quantity":order.quantity,
                "order_statuses":order.order_status.value,
            }

        return jsonable_encoder(custom_order)
    

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only superadmin can you see")


