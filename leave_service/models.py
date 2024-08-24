from datetime import datetime
from fastapi.security import OAuth2,SecurityScopes
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import BaseModel
from typing import Dict, List, Optional
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
    getdate:datetime|None

class OAuth2PasswordBearerWithCookie(OAuth2):
    """
    This class is taken directly from FastAPI:
    https://github.com/tiangolo/fastapi/blob/26f725d259c5dbe3654f221e608b14412c6b40da/fastapi/security/oauth2.py#L140-L171
    
    The only change made is that authentication is taken from a cookie
    instead of from the header!
    """
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[Dict[str, str]] = None,
        description: Optional[str] = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> Optional[str]:
        # IMPORTANT: this is the line that differs from FastAPI. Here we use 
        # `request.cookies.get(settings.COOKIE_NAME)` instead of 
        # `request.headers.get("Authorization")`
        authorization: str = request.cookies.get(settings.COOKIE_NAME) 
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param


oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="token",
                                               scopes={"employee": "employee rights","manager":"manager rights"},)

def get_current_user_from_cookie(request: Request) -> User:
    """
    Get the current user from the cookies in a request.
    
    Use this function from inside other routes to get the current user. Good
    for views that should work for both logged in, and not logged in users.
    """
    token = request.cookies.get(settings.COOKIE_NAME)
    user = decode_token(token)
    return user
async def get_current_user_from_token(security_scopes: SecurityScopes,token: str = Depends(oauth2_scheme)) -> User:
   
    """
    Get the current user from the cookies in a request.

    Use this function when you want to lock down a route so that only 
    authenticated users can see access the route.
    """
    print("hello")
    user = decode_token(security_scopes,token)
    return user

def decode_token(security_scopes: SecurityScopes,token: str) -> User:
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    
    token = token.removeprefix("Bearer").strip()
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        id: str = payload.get("id")
        token_scopes = payload.get("rolename", [])
        email:str=payload.get("email")
       
        idprofile:str=payload.get("idprofile")
       
        print(id)
        print(token_scopes)
        if token_scopes not in security_scopes.scopes:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
            headers={"WWW-Authenticate": authenticate_value},
        )
        if id is None:
            raise credentials_exception
    except JWTError as e:
        print(e)
        raise credentials_exception
    user=User(id=id,email=email,password="",created_date="",idprofile=idprofile,rolename=token_scopes,statuslogin=1,getdate=None)
    #user = get_user(id)
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