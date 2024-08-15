
from .forms import LoginForm
import db
from .models import User,get_current_user_from_cookie,get_current_user_from_token
from fastapi import APIRouter,Request,status,Response,Depends,FastAPI,Security
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from .models import create_access_token,User,user_avatar
from typing import Dict
from ultils import settings,file_path_default
from typing import Annotated
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import datetime
from fastapi.staticfiles import StaticFiles
import requests
auth = APIRouter()
@auth.get("/",tags=["authentication"], response_class=HTMLResponse)
def index():
    return RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)

@auth.get("/signin",tags=["authentication"], response_class=HTMLResponse)
def signin_get():
    response = requests.get(
            "http://localhost:8001/signin"
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)

@auth.post("resgisteraccersstoken",tags=["authentication"])
def resgister_for_access_token(response: Response, user: OAuth2PasswordRequestForm = Depends()) -> Dict[str, str]:
    access_token = create_access_token(data={"id":user.id,"rolename":user.rolename})
    response.set_cookie(
        key=settings.COOKIE_NAME, 
        value=f"Bearer {access_token}", 
        domain=".localhost",
        path="/",
        httponly=True
    )  
    #return response
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}

@auth.post("/signin",tags=["authentication"], response_class=HTMLResponse)
async def signin(request: Request):   
    try:
        current_user = get_current_user_from_cookie(request)
    except:
        current_user = None
    form = LoginForm(request)
    await form.load_data()
    if await form.is_valid():
      
        conn=db.connection()
        cursor=conn.cursor()
        sql="select a.id,r.rolename from account a join roleuser r on a.role_id=r.id where a.email=%s and a.password=%s"
        values=(form.email, form.password,)
        cursor.execute(sql,values)
        id_user =cursor.fetchone()
        conn.commit()
        conn.close()
        if id_user is not None:
    
            user=User(id=id_user[0],rolename=id_user[1])
            response= RedirectResponse(url=f"/authorizationUser",status_code=status.HTTP_302_FOUND)
            
            #response= RedirectResponse(url=VERIFY_2FA_URL)
            resgister_for_access_token(response=response, user=user)
            return response
            
        else:
            messages=[("danger","Invalid username and/or password.")]
            response= RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)
            return response


@auth.get("/authorizationUser",tags=['authentication'])
async def authorizationUser(request:Request,response:Response,
                            current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from profileuser where idaccount=%s"
    value=(current_user.id,)
    cursor.execute(sql,value)
    user_temp=cursor.fetchone()
    
    #   set image path
    image_path_value=None
    found_avatar = user_avatar.find_picture_name_by_id(current_user.idprofile)
    if found_avatar and found_avatar[2] != "":
        response.set_cookie(key="image_path_session", value=str(found_avatar[2]))
        image_path_value=found_avatar[2]
    else:
        image_path_value=file_path_default
        response.set_cookie(key="image_path_session", value=file_path_default)
    
    fullname_value=user_temp[1]
    response.set_cookie(key="fullname_session", value=str(user_temp[1]))
        
    conn=db.connection()
    cursor=conn.cursor()
    sql="insert into calendar(checkin,idaccount) values(%s,%s)"
    value=(datetime.now(),user_temp[0],)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    new_id = cursor.lastrowid
        
    if current_user.rolename=="employee":
        response=RedirectResponse(url="/home",status_code=status.HTTP_302_FOUND)
        response.set_cookie(key="checkinid", value=new_id)
        response.set_cookie(key="roleuser", value="employee")
        response.set_cookie(key="image_path_session", value=image_path_value)
        response.set_cookie(key="fullname_session", value=fullname_value)
        return response
        
        

    elif current_user.rolename=="manager":
        response= RedirectResponse(url='/home')
        response.set_cookie(key="checkinid", value=new_id)
        response.set_cookie(key="roleuser", value="manager")
        response.set_cookie(key="image_path_session", value=image_path_value)
        response.set_cookie(key="fullname_session", value=fullname_value)
        return response
    else:
        return "You have not been granted access to the resource"
    
@auth.get("/home",tags=['user'], response_class=HTMLResponse)
async def home(request:Request,
               current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    cookies = request.cookies
    response = requests.get(
            "http://localhost:8001/home",
            cookies=cookies
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)

@auth.get("/calendarcheckin",tags=['user'], response_class=HTMLResponse)
async def calendarcheckin(request:Request,
               current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    cookies = request.cookies
    response = requests.get(
            "http://localhost:8001/calendarcheckin",
            cookies=cookies
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)

@auth.get("/logout",tags=['user'], response_class=HTMLResponse)
async def logout_get(request:Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    response = RedirectResponse(url="/")
    response.delete_cookie(settings.COOKIE_NAME)
    response.delete_cookie('roleuser')
    response.delete_cookie('rolemanager')
    response.delete_cookie('image_path_manager')
    response.delete_cookie('fullname_manager')
    response.delete_cookie('image_path_session')
    response.delete_cookie('fullname_session')

    conn=db.connection()
    cursor=conn.cursor()
    sql="update calendar set checkout=%s where id=%s"
    value=(datetime.now(),int(request.cookies.get("checkinid")),)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    return response
# @auth.post("/signin",tags=["authentication"], response_class=HTMLResponse)
# async def signin(request: Request):
#     form_data = await request.form()
#     response = requests.post(
#             "http://localhost:8001/signin",data=form_data
#         )
#     response.raise_for_status()
#     return HTMLResponse(content=response.text, status_code=response.status_code)
