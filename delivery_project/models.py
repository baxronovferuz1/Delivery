from sqlalchemy import Column,Integer,Boolean,Text,String,ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types import ChoiceType
from database import Base



class User(Base):
    __tablename__="user"
    id=Column(String, primary_key=True)
    username=Column(String(String(25), unique=True))
    email=Column(String(80), unique=True)
    password=Column(Text, nullable=True)
    is_staff=Column(Boolean, default=False)
    is_active=Column(Boolean, default=False)