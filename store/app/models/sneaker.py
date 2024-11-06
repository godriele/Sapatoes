from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime
from models import Base

class Sneaker(Base):
    __tablename__ ='sneakers'
    
    id = mapped_column(Integer, primary_key=True)
    sneakers_id = mapped_column(String, unique=True, nullable=True)
    brand = mapped_column(String, nullable=False)
    name = mapped_column(String, nullable= False)
    colorway = mapped_column(String)
    gender = mapped_column(String)
    release_date = mapped_column(DateTime)
    retail_price = mapped_column(Float)
    resale_price = mapped_column(Float)
    shoe_type = mapped_column(String)
    style_code = mapped_column(String, unique=True)
    description = mapped_column(String)
    image_url = mapped_column(String)
    sizes = mapped_column(String)
    
    orders = relationship("Orders", back_populates="sneaker")