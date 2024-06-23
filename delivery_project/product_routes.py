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
    

