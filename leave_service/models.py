from datetime import datetime

from pydantic import BaseModel
import db
from jose import JWTError, jwt
import db
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi import Depends, FastAPI, HTTPException, Request, Response, status,Security

from ultils import settings
class User(BaseModel):
    id:int
    email:str=None
    password:str=None
    created_date:str=None
    rolename:str=None
    idprofile:int=None
    statuslogin:bool=False
    getdate:datetime=None

def get_current_user_from_cookie(request: Request) -> User:
    """
    Get the current user from the cookies in a request.
    
    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    user = decode_token(token)
    return user

def decode_token(token: str) -> User:
   
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id: str = payload.get("id")
        if id is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    
    user = get_user(id)
    return user

def get_user(id:str) -> User:
    conn=db.connection()
    cursor=conn.cursor()
    sql="select a.*,p.id,r.rolename from account a join profileuser p on a.id=p.idaccount join roleuser r on r.id=a.role_id where a.id=%s"
    value=(id,)
    cursor.execute(sql,value)
    user_temp=cursor.fetchone()
    conn.commit()
    conn.close()
    
    if user_temp is not None:
        user=User(id=user_temp[0],email=user_temp[1],password=user_temp[2],created_date=user_temp[3].strftime('%Y-%m-%d %H:%M:%S'),idprofile=user_temp[5],rolename=user_temp[6],statuslogin=1,getdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    else:
        user = User(
            id=0,
            email="",
            password="",
            created_date="",
            idprofile=0,
            rolename="",
            statuslogin=0,
            getdate=""
        )
    
    return user