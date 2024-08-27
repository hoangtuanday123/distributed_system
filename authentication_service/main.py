from forms import LoginForm
import db
from models import User,get_current_user_from_cookie,get_current_user_from_token
from fastapi import APIRouter,Request,status,Response,Depends,FastAPI,Security,Form,HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from models import create_access_token,User,user_avatar
from typing import Dict
from ultils import settings,file_path_default
from typing import Annotated
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import datetime
from fastapi.responses import JSONResponse
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
    access_token = create_access_token(data={"id":user.id,"rolename":user.rolename,"email":user.email,"idprofile":user.idprofile
                                             })
    response.set_cookie(
        key=settings.COOKIE_NAME, 
        value=f"Bearer {access_token}", 
        domain=".localhost",
        path="/",
        httponly=True
    )  
    #return response
    return {settings.COOKIE_NAME: access_token, "token_type": "bearer"}

@app.get("/getprofile/{idaccount}",tags=["authentication"], response_class=HTMLResponse)
async def getprofile(idaccount,
                            current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    conn=db.connection()
    cursor=conn.cursor()
    sql="select * from profileuser where idaccount=%s"
    value=(int(idaccount),)
    cursor.execute(sql,value)
    user_temp=cursor.fetchone()
    return JSONResponse(content={"profile": user_temp})
    return str(user_temp)


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
        sql="select a.*,p.id,r.rolename from account a join profileuser p on a.id=p.idaccount join roleuser r on r.id=a.role_id where a.email=%s and a.password=%s"
        values=(form.email, form.password,)
        cursor.execute(sql,values)
        user_temp =cursor.fetchone()
        conn.commit()
        conn.close()
        if user_temp is not None:
            
            user=User(id=user_temp[0],email=user_temp[1],password=user_temp[2],created_date=user_temp[3].strftime('%Y-%m-%d %H:%M:%S'),idprofile=user_temp[5],rolename=user_temp[6],statuslogin=1,getdate=datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            response= RedirectResponse(url=f"/authorizationUser",status_code=status.HTTP_302_FOUND)
            
            #response= RedirectResponse(url=VERIFY_2FA_URL)
            resgister_for_access_token(response=response, user=user)
            return response
            
        else:
            messages=[("danger","Invalid username and/or password.")]
            response= RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)
            return response
    return RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)
        
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
    value=(datetime.now(),current_user.id,)
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

@app.get("/logout",tags=['user'], response_class=HTMLResponse)
async def logout_get(request:Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    
    response = RedirectResponse(url="/signin",status_code=status.HTTP_302_FOUND)
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



@app.get("/profile", tags=["manageProfile"], response_class=HTMLResponse)
async def displayAllProfile(request: Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    
    role = request.cookies.get("roleuser")
    conn = db.connection()
    cursor = conn.cursor()
    sql = " "
    if role == "manager":
        sql = "select * from profileuser"
        cursor.execute(sql)
        profiles = cursor.fetchall()
        conn.commit()
        conn.close()
        context = {
        "request": request,
        "profiles": profiles,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
        }
        return templates.TemplateResponse("authentication/displayAllProfiles.html",context)
    elif role == "employee":
        sql = "select * from profileuser where idaccount = %s"
        id = (current_user.id,)
        print(current_user.id)
        cursor.execute(sql,id)
        profiles = cursor.fetchall()
        conn.commit()
        conn.close()
        context = {
        "request": request,
        "profiles": profiles,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
        }
    
    return templates.TemplateResponse("authentication/displayAllProfiles.html",context)
    
    # sql = "select * from profileuser"
    


@app.get("/updateProfile", tags=["manageProfile"],response_class=HTMLResponse)
async def displayCurrentProfile(request:Request,profileId: int, current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):

    conn = db.connection()
    cursor = conn.cursor()
    sql = "select p.id, p.fullname, p.cccd, p.tax, p.phone, p.address, p.bankcode, p.bankname, r.id, r.rolename from profileuser p, account a, roleuser r where p.idaccount = a.id and a.role_id = r.id and p.id = %s"
    id = (profileId,)
    cursor.execute(sql,id)
    profiles = cursor.fetchall()

    sql = "select * from roleuser where rolename !=(select r.rolename from profileuser p, account a, roleuser r where p.idaccount = a.id and a.role_id = r.id and p.id = %s)"
    id = (profileId,)
    cursor.execute(sql,id)
    roleusers = cursor.fetchall()

    context = {
        "request": request,
        "profileId":profileId,
        "profiles": profiles,
        "roleusers": roleusers,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("authentication/updateProfile.html",context)

@app.get("/viewProfile", tags=["manageProfile"],response_class=HTMLResponse)
async def displayCurrentProfile(request:Request,profileId: int, current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from profileuser where id= %s"
    id = (profileId,)
    cursor.execute(sql,id)
    profiles = cursor.fetchall()
    conn.commit()
    conn.close()
    context = {
        "request": request,
        "profileId":profileId,
        "profiles": profiles,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("authentication/viewProfile.html",context)

# @app.post("/requestUpdate",tags=["manageProfile"],response_class=HTMLResponse)
# async def requestUpdate(request: Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
#     form_method = await request.form()


@app.post("/saveProfileManager",tags=["manageProfile"],status_code=status.HTTP_302_FOUND)
async def updateProfile(
    request: Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])],
    profileId: int = Form(...),
    fullname: str = Form(...),
    nationalId: str = Form(...),
    taxnumber: str = Form(...),
    phonenumber: str = Form(...),
    address: str = Form(...),
    bankcode: str = Form(...),
    bankname: str = Form(...),
    role: int = Form(...)
    ):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "update profileuser set fullname = %s, cccd = %s, tax = %s, phone = %s, address = %s, bankcode = %s, bankname = %s where id = %s"
    value = (fullname,nationalId,taxnumber,phonenumber,address,bankcode,bankname,profileId,)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()

    con1 = db.connection()
    cur1 = con1.cursor()
    sql1 = "select idaccount from profileuser where id = %s"
    val1 = (profileId,)
    cur1.execute(sql1,val1)
    idas = cur1.fetchone()
    x = idas[0]
    
    sql1 = "update account set role_id = %s where id = %s"
    val1 = (role,x,)
    cur1.execute(sql1,val1)
    con1.commit()
    con1.close()
    
    return RedirectResponse(url="/profile",status_code=status.HTTP_302_FOUND)

@app.post("/saveProfileEmployee",tags=["manageProfile"],status_code=status.HTTP_302_FOUND)
async def updateProfile(
    request: Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])],
    profileId: int = Form(...),
    fullname: str = Form(...),
    nationalId: str = Form(...),
    taxnumber: str = Form(...),
    phonenumber: str = Form(...),
    address: str = Form(...),
    bankcode: str = Form(...),
    bankname: str = Form(...),
    
    ):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "update profileuser set fullname = %s, cccd = %s, tax = %s, phone = %s, address = %s, bankcode = %s, bankname = %s where id = %s"
    value = (fullname,nationalId,taxnumber,phonenumber,address,bankcode,bankname,profileId,)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()    
    return RedirectResponse(url="/profile",status_code=status.HTTP_302_FOUND)
# checking whether registeredEmail has already existed 
@app.post("/checkEmail",tags=["manageProfile"])
async def checkEmail(request: Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])]):
    data = await request.json()
    email = data.get("email")

    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from account where email = %s"
    value = (email,)
    cursor.execute(sql,value)
    check = cursor.fetchone()
    conn.commit()
    conn.close()
    if check:
        raise HTTPException(status_code=400, detail="Email already exists")
    return {"detail": "Email is available"}


@app.get("/createAccount",tags=["manageProfile"],response_class=HTMLResponse)
async def displayCreateAccountForm(request:Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])]):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from roleuser"
    cursor.execute(sql)
    roleusers = cursor.fetchall()

    sql = "select count(*) from account where id not in (select idaccount from profileuser)"
    cursor.execute(sql)
    count = cursor.fetchone()
    check = count[0]

    if (check != 0 ):
        return RedirectResponse(url="/addProfile",status_code=status.HTTP_302_FOUND)
    else:
        context = {
            "request": request,
            "roleusers": roleusers,
            "roleuser":request.cookies.get("roleuser"),
            "image_path":request.cookies.get("image_path_session"),
            "fullname":request.cookies.get("fullname_session"),
            "is_authenticated":1,
            "current_user":current_user
        }
        return templates.TemplateResponse("authentication/createAccount.html",context)

@app.post("/createAccount",tags=["manageProfile"])
async def addNewAccount(
    request:Request,
    current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])]
    ):


    data = await request.json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")
    conn = db.connection()
    cursor = conn.cursor()
    sql = "insert into account(email,password,created_date,role_id) values (%s,%s,curdate(),%s)"
    value = (email,password,role,)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    

@app.get("/addProfile",tags=["manageProfile"],response_class=HTMLResponse)
async def displayAddProfileForm(request:Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])]):
    conn = db.connection()
    cursor = conn.cursor()
    sql = "select * from account where id not in (select idaccount from profileuser) order by id desc"
    cursor.execute(sql)
    emails = cursor.fetchall()
    conn.commit()
    conn.close()
    context = {
        "request": request,
        "emails": emails,
        "roleuser":request.cookies.get("roleuser"),
        "image_path":request.cookies.get("image_path_session"),
        "fullname":request.cookies.get("fullname_session"),
        "is_authenticated":1,
        "current_user":current_user
    }
    return templates.TemplateResponse("authentication/addProfile.html",context)

@app.post("/addProfile",tags=["manageProfile"],status_code=status.HTTP_302_FOUND)
async def addProfile(request:Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])],
                    email: int = Form(...),
                    fullname: str = Form(...),
                    nationalId: str = Form(...),
                    taxnumber: str = Form(...),
                    phonenumber: str = Form(...),
                    address: str = Form(...),
                    bankcode: str = Form(...),
                    bankname: str = Form(...),
                    ):
    
    conn = db.connection()
    cursor = conn.cursor()
    sql = "insert into profileuser(fullname,cccd,tax,phone,address,bankcode,bankname,idaccount) value (%s,%s,%s,%s,%s,%s,%s,%s)"
    value = (fullname,nationalId,taxnumber,phonenumber,address,bankcode,bankname,email,)
    cursor.execute(sql,value)
    conn.commit()
    conn.close()
    return RedirectResponse(url="/profile",status_code=status.HTTP_302_FOUND)

