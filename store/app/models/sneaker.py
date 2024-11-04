from sqlalchemy.orm import mapped_column
from sqlalchemy import Integer, String, Float, Date
from database import Base
import requests
from sqlalchemy.orm import sessionmaker
from database import engine

class Sneaker(Base):
    __tablename__ = 'sneaker'
    
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100), nullable=False)
    brand = mapped_column(String(50), nullable=False)
    styleID = mapped_column(String(50), unique=True, nullable=False)
    releaseData = mapped_column(Date, nullable=True)
    retailPrice = mapped_column(Float, nullable=True)
    images = mapped_column(String)
    description = mapped_column(String)
    category = mapped_column(String(50), nullable=True) 
    
    def __repr__(self):
        return f"<Sneaker(name='{self.name}', brand='{self.brand}', styleID='{self.styleID}')>"
    


# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

def fetch_and_save_sneakers(keyword, limit=10):
    sneaks_api_url = f"https://api.sneaks-api.com/products?keyword={keyword}&limit={limit}"
    
    response = requests.get(sneaks_api_url)
    
    if response.status_code != 200:
        print("Error fetching data from Sneaks API:", response.status_code)
        return

    products = response.json()
    
    for product in products:
        sneaker = Sneaker(
            name=product.get('name'),
            brand=product.get('brand'),
            styleID=product.get('styleID'),
            releaseDate=product.get('releaseDate'),  # Adjust based on actual data format
            retailPrice=product.get('retailPrice'),
            images=','.join(product.get('images', [])),  # Assuming images is a list
            description=product.get('description', ''),
            category=product.get('category', '')
        )

        session.add(sneaker)
    
    session.commit()
    print(f"{len(products)} sneakers saved to the database.")

# Example usage
fetch_and_save_sneakers("Yeezy Cinder")
