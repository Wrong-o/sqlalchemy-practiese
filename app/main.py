from database import get_db  # Make sure to import get_db correctly
from fastapi import Depends, FastAPI, HTTPException, status
from models import Product, Role, User
from passlib.context import CryptContext
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

app = FastAPI()


def create_user(email: str, password: str, db: Session):
    user = User(email=email)
    user.set_password(password)
    db.add(user)
    db.commit()
    print(f"User {email} created")


def verify_user_login(email: str, password: str, db: Session) -> bool:
    user = db.query(User).filter_by(email=email).first()
    if user and user.check_password(password):
        return True
    return False


@app.post("/login/")
def login(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    if not verify_user_login(email=email, password=password, db=db):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    if user.role_relation.role_name == "admin":
        return {"message": "Welcome, admin"}
    elif user.role_relation.role_name == "user":
        return {"message": "Welcome, user!"}
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Forbidden access",
        )


@app.post("/register/")
def register_user(email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:  # If the user with this email exists, raise an error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered",
        )

    try:
        create_user(email=email, password=password, db=db)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the user",
        )
