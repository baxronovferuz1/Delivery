from database import engine,Base
from models import User,Order,Product
# from sqlalchemy import create_engine

# engine = create_engine('postgresql://postgres:feruz2003@localhost/delivery_db', echo=True)

Base.metadata.create_all(bind=engine)