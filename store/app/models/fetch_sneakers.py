import requests
from sqlalchemy.orm import sessionmaker
from config import db
from sneaker import Sneaker
from datetime import datetime

# Create a new session
Session = sessionmaker(bind=db.engine)

def fetch_and_save_sneakers(keyword, limit=10):
    sneaks_api_url = f"https://api.sneaks-api.com/products?keyword={keyword}&limit={limit}"
    
    try:
        response = requests.get(sneaks_api_url)
        response.raise_for_status()  # Raises an error for bad responses (4xx, 5xx)

        products = response.json().get('products', [])  # Ensure you're accessing the correct key
        
        session = Session()  # Create a new session for the operation
        
        for product in products:
            sneaker = Sneaker(
                name=product.get('name'),
                brand=product.get('brand'),
                styleID=product.get('styleID'),
                releaseDate=datetime.strptime(product.get('releaseDate'), "%Y-%m-%d") if product.get('releaseDate') else None,  # Adjust date parsing
                retailPrice=product.get('retailPrice'),
                images=','.join(product.get('images', [])),  # Assuming images is a list
                description=product.get('description', ''),
                category=product.get('category', '')
            )

            session.add(sneaker)
        
        session.commit()
        print(f"{len(products)} sneakers saved to the database.")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching sneakers: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        session.close()  # Ensure the session is closed after the operation

# Example usage
if __name__ == "__main__":
    fetch_and_save_sneakers("Yeezy Cinder")
