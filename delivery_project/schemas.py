from pydantic import BaseModel
from typing import Optional


class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_staff: Optional[bool]
    is_active: Optional[bool]

    class Config:
        orm_mode = True
        # from_attributes = True
        schema_extra = {  # example for user
            "example": {
                "username": "hasan",
                "email": "hasan@gmail.com",
                "password": "hasan123",
                "is_staff": False,
                "is_active": True,
            }
        }


class Settings(BaseModel):
    authjwt_secret_key: str = (
        "915491a7ff481a64d067c33b4256df6c160b4d2126128db94dce5590ee6eb191"
    )


class LoginModel(BaseModel):
    username_or_email: str
    password: str


class OrderModel(BaseModel):
    id: Optional[int]
    quantity: int
    order_statuses: Optional[str] = "PENDING"
    user_id: Optional[int]
    product_id: int

    class Config:
        orm_model = True
        schema_extra = {
            "example": {
                "quantity": 2,
            }
        }


class OrderStatusModel(BaseModel):
    order_statuses: Optional[str] = "PENDING"

    class Config:
        orm_model = True
        schema_extra = {"example": {"order_statuses": "PENDING"}}


class ProductModel(BaseModel):
    id: Optional[int]
    name: str
    price: int

    class Config:
        orm_model = True
        schema_extra = {"example": {"name": "Pizza", "price": 30000}}
