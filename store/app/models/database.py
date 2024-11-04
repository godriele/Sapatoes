from sqlalchemy.orm import declarative_base
from flask_sqlalchemy import SQLAlchemy
from config import db

Base = declarative_base()

db = SQLAlchemy()


