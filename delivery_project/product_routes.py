from fastapi import APIRouter,Depends,status
from fastapi_jwt_auth import AuthJWT
from models import User,Product
from schemas import ProductModel
from database import session,engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

product_router = APIRouter(
    prefix="/product",
)

session=session(bind=engine)

@product_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(product:ProductModel, Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail="Enter valid access token")
    
    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        create_new_product=Product(
            name=product.name,
            price=product.price
        )
        session.add(create_new_product)
        session.commit()

        responce_data={
            "success":True,
            "code":201,
            "message":"Product is cretaed successfully",
            "data":{
                "id":create_new_product.id,
                "name":create_new_product.name,
                "price":create_new_product.price
            }
        }

        return jsonable_encoder(responce_data)
    
    else:

        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only Admin can add new product")
    

@product_router.get("/list", status_code=status.HTTP_200_OK)
async def product_list(Authorize:AuthJWT=Depends()):


    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,  detail="Enter valid access token")
    
    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        products=session.query(Product).all()

        response_data=[
            {
                "id":product.id,
                "name":product.name,
                "price":product.price
            }
            for product in products
        ]

        return jsonable_encoder(response_data)
    
    else:
        return HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only admin can see products list")



@product_router.get("/{id}")
async def product_by_id(id:int , Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized,enter valid access token")
    
    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        product=session.query(Product).filter(Product==id).first()
        if product:
            response={
                "id":product.id,
                "name":product.name,
                "price":product.price
            }

        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No product found for this id {id}")

        return jsonable_encoder(response)
    

    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only superadmin can you see")



@product_router.delete("/{id}",status_code=status.HTTP_200_OK)
async def delete_product(id:int , Authorize:AuthJWT=Depends()):

    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="The user is not authorized,enter valid access token")
    
    user=Authorize.get_jwt_subject()
    current_user=session.query(User).filter(User.username==user).first()

    if current_user.is_staff:
        product=session.query(Product).filter(Product.id==id).first()
        if product:
            session.delete(product)
            session.commit()
            data={
                "success":True,
                "code":200,
                "message":f"ID {id} has been deleted",
                "data":None
            }
            return jsonable_encoder(data)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"ID {id} is not found")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only superadmin can delete")
