from typing import List
from pydantic import BaseModel

#creating schemas for blog
class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    user_id: int
    
    class Config:
        from_attributes = True
        
#Creating schemas for user       
class UserBase(BaseModel):
    username: str
    email:str
    
class UserCreate(UserBase):
    password: str
    
class User(UserCreate):
    id: int
    is_active: bool
    blogs: List[Blog] = []
    
    class Config:
        from_attributes = True
        
    