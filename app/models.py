from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

#if table not already then it will be created
class Post(Base):   
    __tablename__="posts"

    id=Column(Integer, primary_key=True, nullable=False)
    title=Column(String, nullable=False)
    content=Column(String, nullable=False)
    published=Column(Boolean, server_default="True", nullable=False)
    created_at=Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()'))
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    #we need to pass the tablename.column, then we mention what to do on delete, fir ek null wala bhi kar hi do
    owner = relationship("Users") #this users is the class Users(Base) wala Users
    #this is gonna figure out the relationship to the user, fetch the user based off the owner_id

class Users(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, nullable=False)
    email=Column(String, nullable=False, unique=True)
    password=Column(String, nullable=False)
    created_at=Column(TIMESTAMP (timezone=True), nullable=False, server_default=text('now()'))
    phone_number=Column(String)

class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)