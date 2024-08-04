
from fastapi import APIRouter,Request,status,Response,Depends,Security
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
import requests
from datetime import datetime
from typing import Annotated
from authentication.models import User,get_current_user_from_cookie,get_current_user_from_token
import httpx
timesheet = APIRouter()
templates = Jinja2Templates(directory="templates")


@timesheet.get("/updatetimesheet",tags=["timesheet"], response_class=HTMLResponse)
def timesheet_get(request: Request,current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    cookies = request.cookies
    response = requests.get(
            "http://localhost:8002/updatetimesheet",cookies=cookies
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)

@timesheet.post("/updatetimesheet",tags=["timesheet"], response_class=HTMLResponse)
async def timesheet_post(request: Request):
    form_method= await request.form()
    cookies = request.cookies
    selecttiontasks=form_method.getlist('checkbox')
    form_data = dict(form_method)
    form_data['checkbox'] = selecttiontasks
    async with httpx.AsyncClient() as client:
        response =await   client.post(
            "http://localhost:8002/updatetimesheet",
            data=form_data,
            cookies=cookies
        )
        if response.status_code == status.HTTP_302_FOUND:
            redirect_url = response.headers.get('Location')
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.raise_for_status()
    
    return HTMLResponse(content=response.text, status_code=response.status_code)
    


@timesheet.get("/addtimesheet",tags=["timesheet"], response_class=HTMLResponse)
async def addtimesheet_get(request: Request,
                           current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    cookies = request.cookies
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://localhost:8002/addtimesheet",
            cookies=cookies
        )
        response.raise_for_status()
    
    return HTMLResponse(content=response.text, status_code=response.status_code)


@timesheet.post("/addtimesheet",tags=["timesheet"], response_class=HTMLResponse)
async def addtimesheet(request: Request,
                       current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    cookies = request.cookies
    form=await request.form()
    async with httpx.AsyncClient() as client:
        response =await  client.post(
                "http://localhost:8002/addtimesheet",cookies=cookies,data=form
            )
        if response.status_code == status.HTTP_302_FOUND:
            redirect_url = response.headers.get('Location')
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)
    





@timesheet.get("/timesheetview",tags=["timesheet"], response_class=HTMLResponse)
async def timesheetview_get(request: Request,
                            current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])]):
    cookies = request.cookies
    response = requests.get(
            "http://localhost:8002/timesheetview",cookies=cookies
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)

@timesheet.post("/timesheetview",tags=["timesheet"], response_class=HTMLResponse)
async def timesheetview(request: Request,
                        current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    form_method=await request.form()
    cookies = request.cookies
    selecttiontasks=form_method.getlist('checkbox')
    form_data = dict(form_method)
    form_data['checkbox'] = selecttiontasks
    async with httpx.AsyncClient() as client:
        response =await  client.post(
                "http://localhost:8002/timesheetview",cookies=cookies,data=form_data
            )
        if response.status_code == status.HTTP_302_FOUND:
            redirect_url = response.headers.get('Location')
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)
    

