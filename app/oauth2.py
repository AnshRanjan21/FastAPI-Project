from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key  #documentation se uthaya hai
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes     #30 mins, if we dont profile user will be kept loggedin for infinity

def create_access_token(data: dict):
    to_encode = data.copy() #to_encode alag banaya taki we can use data later if required

    expire=datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) #timedelta is used to perform arithematic operations on time
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token : str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id:str = str(payload.get("user_id"))  #since payload is storing token content as a dict
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)  #first id is schema wali id, 2nd id is iss func ka variable id
    
    except JWTError:
        raise credentials_exception
    
    return token_data
    

def get_current_user(token:str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
# this func is supposed to verify token and also fetch the user from the database
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="could not validate credentials",
                                          headers={"WWW-Authenticate" : "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()
    return user
