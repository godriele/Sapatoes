from database import engine
from models import Base
import users
import sneaker
import orders

Base.metadata.create_all(engine)
