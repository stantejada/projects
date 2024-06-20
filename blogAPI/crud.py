from db import models, schemas
from sqlalchemy.orm import Session
import jwt

#setting hashed ()
KEY = "a32f56f29eb99c1adc735c348972d28f5dd786c87ea243d6bcd4d86fc092238c"
ALGORITHM = "HS256"


#getting user by id
def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

#getting user by email
def fetch_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

#getting all users
def get_all_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

#getting all blogs
def get_all_blogs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Blog).offset(skip).limit(limit).all()

#create new users
def create_new_user(db: Session, user: schemas.UserCreate):
    hashed_password = jwt.encode(payload={"hashed_password":user.password}, key=KEY, algorithm=ALGORITHM)
    
    db_user = models.User(username = user.username, email = user.email, password = hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_new_blog(db: Session, blog: schemas.BlogCreate, user_id:int):
    db_blog = models.Blog(**blog.model_dump(), user_id = user_id)
    db.add(db_blog)
    db.commit()
    db.refresh(db_blog)
    return db_blog

def update_user_by_id(db: Session, user: schemas.User, db_user:models.User):
    db_user.username = user.username
    db_user.email = user.email
    ### Create a function to help me to validate if user wants to change its dates: pending ###
    db_user.password = jwt.encode(payload={"hashed_password": user.password}, key=KEY, algorithm=ALGORITHM)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_blog_by_id(db: Session, blog_id: int):
    return db.query(models.Blog).filter(models.Blog.id == blog_id).first()

def update_blog_by_user(db: Session, user_id: int, blog:schemas.Blog, db_blog:models.Blog):
    if db_blog.user_id == user_id:
        db_blog.title = blog.title
        db_blog.content = blog.content
        db.commit()
        db.refresh(db_blog)
    else:
        return None
    return db_blog

def delete_user_by_id(db: Session, user: models.User):
    db.delete(user)
    db.commit()
    