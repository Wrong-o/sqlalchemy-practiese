from passlib.hash import bcrypt
from sqlalchemy import Column, Float, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Product(Base):
    __tablename__ = "product_table"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(255))
    manual = Column(String)
    category = Column(String(255))


class User(Base):
    __tablename__ = "users_table"

    id = Column(Integer, primary_key=True)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)

    def set_password(self, password: str):
        """Hash the password before storing"""
        self.password_hash = bcrypt.hash(password)

    def check_password(self, password: str) -> bool:
        """Check if the password matches stored hash"""
        return bcrypt.verify(password, self.password_hash)
