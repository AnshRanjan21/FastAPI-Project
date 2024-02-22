from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class PostsBase(BaseModel):
    #id: int
    title : str
    content : str
    published : bool = True
    #were are not adding userid(ownerid) in here because it would also require our user to enter userid while creating a post 
    # we should rather get that automatically from out token and logic

class PostsCreate(PostsBase):
    pass
    #remember owner_id yaha nahi likhna, it would mean that user program expects user to enter owner_id himself

class UserResponse(BaseModel):  #adding this above postresponse so that it can call this pydantic model in response
    id: int
    email: EmailStr
    created_at : datetime
    class Config: 
        from_attributes = True


class PostsResponse(PostsBase):
    #inheritence forgives me from writing title, content, published again and again
    id: int
    created_at: datetime
    owner_id: int
    owner:UserResponse
    class Config: #by default pydantic model will only read dict. This will tell pydantic to ignore the fact ki it's getting ORM model during create post
        from_attributes = True #UserWarning: Valid config keys have changed in V2: 'orm_mode' has been renamed to 'from_attributes'

class PostOut(BaseModel):
    Post : PostsResponse
    votes : int
    class Config: 
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email : EmailStr
    password : str

class Token(BaseModel):   #since we expect the user to send tokens as well, best to define a schema for it 
    access_token : str
    token_type : str

class TokenData(BaseModel): # for the data within the token
    id: Optional[str] = None

class Vote(BaseModel):
    post_id : int
    #dir : conint(le=1 , ge=0)    isme runtime error toh nahi aara but yellow underline error nahi hat raha
    dir: int = Field(ge=0, le=1)
    