from .. import models, schemas, utils
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users", # this allows us to assign a prefix because sometimes urls can get very long and tiresome to type again and again
    tags=["Users"]  # this groups together all users wale operations
)

@router.post("/signup", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate , db: Session = Depends(get_db)):
    hashed_password=utils.hash(user.password)
    user.password=hashed_password
    
    new_user=models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    #CISNCSS
    return new_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id:int,  db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No such user with id: {id} exists")
    return user