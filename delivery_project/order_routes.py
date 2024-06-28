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
        product=order.product_id
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
            "product":{
                "id":new_order.product.id,
                "name":new_order.product.name,
                "price":new_order.product.price
            },
            "quantity":new_order.quantity,
            "order_statuses":new_order.order_statuses,
            "total_price":new_order.quantity*new_order.product.price
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
                "product":{
                    "id":order.product.id,
                    "name":order.product.name,
                    "price":order.product.price
                },
                "quantity":order.quantity,
                "order_statuses":order.order_statuses.value,
                "total_price":order.quantity*order.product.price
            }
            for order in orders
        ]
        return jsonable_encoder(orders)
    
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only superadmin can see all orders") #The user is authorized, but does not have permission



@order_router.get("/{id}", status_code=status.HTTP_200_OK)
async def order_by_id(id:int , Authorize:AuthJWT=Depends()):


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized,enter valid access token")
    
    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        order=session.query(Order).filter(Order.id==id).first()
        if order:
            custom_order={
                    "id":order.id,
                    "user":{
                        "id":order.user.id,
                        "username":order.user.username,
                        "email":order.user.email
                    },
                    "product":{
                        "id":order.product.id,
                        "name":order.product.name,
                        "price":order.product.price
                    },
                    "quantity":order.quantity,
                    "order_statuses":order.order_statuses.value,
                    'total_price':order.quantity*order.product.price
                }

            return jsonable_encoder(custom_order)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No order found for this id {id}")

            
    

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only superadmin can you see")


@order_router.put("/{id}/update", status_code=status.HTTP_200_OK)
async def update_order(id:int, order:OrderModel, Authorize:AuthJWT=Depends):

    try:
        Authorize.jwt_required
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter access token!")
    
    
    username=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==username).first()


    order_to_update=session.query(Order).filter(Order.id==id).first()
    if order_to_update.user != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You can not change other's order")
    


    order_to_update.quantity=order.quantity
    order_to_update.product_id=order.product_id
    session.commit()

    response={
        "success":True,
        "code":200,
        "message":"Succesfully updated",
        "data":{
            "id":order.id,
            "quantity":order.quantity,
            "product":order.product_id,
            "order_status":order.order_statuses,
        }
    }
    return jsonable_encoder(response)


@order_router.patch("{id}/update_status", status_code=status.HTTP_200_OK)
async def update_order_status(id:int, order=OrderStatusModel, Authorize:AuthJWT=Depends()):


    try:
        Authorize.jwt_required
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter access token!")
    
    
    username=Authorize.get_jwt_subject()
    user=session.query(User).filter(User.username==username).first()

    if user.is_staff:
        previous_status=session.query(Order).filter(Order.id==id).first()
        previous_status.order_statuses.value = order.order_statuses
        session.commit()

        response={
            "status":True,
            "code":200,
            "message":"user order status successfully updated",
            "data":{
                "id":previous_status.id,
                "order_status":previous_status.order_statuses
            }
        }

        return jsonable_encoder(response)



    





