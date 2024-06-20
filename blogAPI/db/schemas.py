from typing import List
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class Blog(BlogBase):
    id: int
    user_id: int
    
    class Config:
        orm_mode = True
        
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
        orm_mode = True
        
    