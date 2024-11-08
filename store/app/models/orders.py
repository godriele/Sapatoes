from sqlalchemy.orm import mapped_column, relationship
from sqlalchemy import String, Integer, Float, DateTime, ForeignKey
from models import Base

class Order(Base):
    __tablename__ = 'orders'
    
    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    sneaker_id = mapped_column('Integer', ForeignKey('sneakers.id'), nullable=False)
    quantity = mapped_column(Integer, nullable=False, default=1)
    order_date = mapped_column(DateTime)
    total_price = mapped_column(Float, nullable=False)
    order_summary = mapped_column(String, nullable=False)
    
    user = relationship("User", back_populates="orders")
    sneaker = relationship("Sneaker", back_populates="orders")