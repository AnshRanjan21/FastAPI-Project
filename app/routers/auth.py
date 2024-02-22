from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
# inbuilt faeture of . we dont have to use user_credentials:schemas.UserLogin now
# and we also no longer send cred in body>raw, we send it in body>form data instead
from .. import database, models, utils, schemas, oauth2

router=APIRouter(tags=['Authentication'])

@router.post("/login", response_model=schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm = Depends() , db: Session=Depends(database.get_db)):
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    # for this oauth wala we do user_credentials.username instead of user_credentials.password bcz in this methord everything is 
    #print(user)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not user")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="no match")
    
    access_token= oauth2.create_access_token(data={"user_id" : user.id})

    return{"access_token" : access_token,
           "token_type" : "bearer"}