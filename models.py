from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(50)) 
    refresh_token = Column(String(500), nullable=True)
    properties = relationship(
        "Property",
        back_populates="owner"
    )

class Property(Base):
    __tablename__ = "properties"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    city = Column(String(100))
    rent = Column(Integer)
    description = Column(String(255))
    owner_id = Column(
        Integer,
        ForeignKey("users.id")
    )
    owner = relationship(
        "User",
        back_populates="properties"
    )