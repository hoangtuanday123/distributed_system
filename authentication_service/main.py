from forms import LoginForm
import db
from models import User,get_current_user_from_cookie,get_current_user_from_token
from fastapi import APIRouter,Request,status,Response,Depends,FastAPI,Security
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models import create_access_token,User,user_avatar
from typing import Dict
from ultils import settings,file_path_default
from typing import Annotated
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import datetime
from fastapi.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")
app = FastAPI(
    title='authentication_service', openapi_url='/openapi.json', docs_url='/docs',
    description='authentication_service'
)
app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/",tags=["authentication"], response_class=HTMLResponse)
async def index(request: Request):
    return  RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)

@app.get("/signin",tags=["authentication"], response_class=HTMLResponse)
async def signin_get(request: Request):
    try:
        user = get_current_user_from_cookie(request)
    except:
        user = None
    form = LoginForm(request)
    context={
        "request":request,
        "form":form,
        "is_authenticated":0,
        "current_user":user
    }
    return templates.TemplateResponse("authentication/login.html",context)


@app.post("resgisteraccersstoken",tags=["authentication"])
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



@app.post("/signin",tags=["authentication"], response_class=HTMLResponse)
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
        
@app.get("/authorizationUser",tags=['authentication'])
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



@app.get("/home",tags=['user'], response_class=HTMLResponse)
async def home(request:Request
              ):
    try:
        current_user = get_current_user_from_cookie(request)
    except:
        current_user = None

    context={
        "request":request,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("authentication/homepage.html",context)


@app.get("/calendarcheckin",tags=['user'], response_class=HTMLResponse)
async def calendarcheckin(request:Request,
                          current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from calendar where checkout is not null and idaccount=%s"
    value=(current_user.id,)
    cursor.execute(sql,value)
    calendar_temp=cursor.fetchall()
    conn.commit()
    conn.close()
    calendar = []
    checkin = []

    for temp in calendar_temp:
        total = temp[2] - temp[1]
        total_seconds = total.total_seconds()
        
        if temp[1].date() not in calendar:
            calendar.append(temp[1].date())
            checkin.append([temp[0], temp[1], temp[2], total_seconds])  # Sử dụng danh sách thay vì tuple
        else:
            for a in checkin:
                if a[1].date() == temp[1].date():
                    a[3] = total_seconds + a[3]
                                        
        # hours = int(total_seconds // 3600)
        # minutes = int((total_seconds % 3600) // 60)
        # seconds = int(total_seconds % 60)
        # totalstring=hours+":"+minutes+":"+seconds
    checkinstring=[]
    for i in checkin:
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)
        totalstring=str(hours)+":"+str(minutes)+":"+str(seconds)
        checkinstring.append((i[0],i[1].date().strftime("%Y-%m-%d"),i[2].date().strftime("%Y-%m-%d"),totalstring))
    context={
        "request":request,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "checkinstring":checkinstring,
        "current_user":current_user
    }
    return templates.TemplateResponse("authentication/calendarcheckin.html",context)

        