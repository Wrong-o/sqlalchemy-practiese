from database import session
from models import Product

products = session.query(Product).all()

for product in products:
    print(f"{product.product_id}, {product.product_name}")
