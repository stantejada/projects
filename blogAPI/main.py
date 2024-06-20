from typing import List

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session

from db import models, schemas
from db.database import SessionLocal, engine
from crud import *

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#dependecy
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
        
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db:Session = Depends(get_db)):
    db_user = fetch_user_by_email(db=db,email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already registered")
    return create_new_user(db=db, user=user)

@app.get("/users/", response_model=List[schemas.User])
async def get_users(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    users = get_all_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user= get_user_by_id(db=db, user_id=user_id)
    if db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exist!")
    return db_user

@app.post("/users/{user_id}/blogs", response_model=schemas.Blog)
async def create_blogs(user_id: int, blog: schemas.BlogCreate, db: Session = Depends(get_db)):
    return create_new_blog(db=db, blog=blog, user_id=user_id)

@app.get("/blogs/", response_model=List[schemas.Blog])
async def get_blogs(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
    blogs = get_all_blogs(db=db, skip=skip, limit=limit)
    return blogs

@app.put("/users/{user_id}/", response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserCreate ,db: Session = Depends(get_db)):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exist!")
    return update_user_by_id(db=db, user=user, db_user=db_user)

@app.put("/users/{user_id}/blogs/{blog_id}", response_model=schemas.Blog)
async def update_blog(user_id: int, blog_id: int, blog: schemas.BlogCreate, db: Session=Depends(get_db)):
    db_blog = get_blog_by_id(db=db, blog_id=blog_id)
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_blog == None and db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog or User doesn't exist!")
    
    return update_blog_by_user(db=db, user_id=user_id, blog=blog, db_blog=db_blog)

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = get_user_by_id(db=db, user_id=user_id)
    if db_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not exist!")
    delete_user_by_id(db=db, user=db_user)
    raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="User has been deleted successfully!")