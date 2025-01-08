from database import session
from models import Product, User

products = session.query(Product).all()

for product in products:
    print(f"{product.product_id}, {product.product_name}")


def create_user(email: str, password: str):
    user = User(email=email)
    user.set_password(password)
    session.add(user)
    session.commit()
    print(f"User {email} created")


def verify_user_login(email: str, password: str) -> bool:
    user = session.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        return True
    return False


if is_authenticated:
    print("Logged in")
else:
    print("Not found")
