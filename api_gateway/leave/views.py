from fastapi import APIRouter,Request,status,Response,Depends,Security
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse,JSONResponse
import requests
from datetime import datetime
from typing import Annotated
from authentication.models import User,get_current_user_from_cookie,get_current_user_from_token
import httpx
leave = APIRouter()
templates = Jinja2Templates(directory="templates")

@leave.get("/requestemployee",tags=['Leave management'], response_class=HTMLResponse)
async def requestemployee(request:Request,
                          current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    cookies = request.cookies
    async with httpx.AsyncClient() as client:
        response =await   client.get(
            f"http://localhost:8003/requestemployee",
            cookies=cookies
        )
        if response.status_code == status.HTTP_302_FOUND:
            redirect_url = response.headers.get('Location')
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)



@leave.get("/request/{year}/{type}",tags=["leave"], response_class=HTMLResponse)
async def request_get(request: Request,year,type,
                      current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    cookies = request.cookies
    response = requests.get(
            f"http://localhost:8003/request/{year}/{type}",cookies=cookies
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)


@leave.post("/request/{year}/{type}",tags=["leave"], response_class=HTMLResponse)
async def request_post(request: Request,year,type,
                       current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    form_method=await request.form()
    cookies = request.cookies
    selecttiontasks=form_method.getlist('checkbox')

    form_data = dict(form_method)
    form_data['checkbox'] = selecttiontasks
    async with httpx.AsyncClient() as client:
        response =await   client.post(
            f"http://localhost:8003/request/{year}/{type}",
            data=form_data,
            cookies=cookies
            
        )
        if response.status_code == status.HTTP_302_FOUND:
            redirect_url = response.headers.get('Location')
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.raise_for_status()
    
    return HTMLResponse(content=response.text, status_code=response.status_code)
    
@leave.post('/get_task',tags=['leave'])
async def get_task(request:Request):
    form=await request.form()
    cookies = request.cookies
    async with httpx.AsyncClient() as client:
        response = await client.post("http://localhost:8003/get_task",cookies=cookies,data=form)
        response.raise_for_status()
    
    return JSONResponse(content=response.json(), status_code=response.status_code)
    

@leave.get("/request_addtask/{year}/{type}",tags=['Leave'],status_code=status.HTTP_302_FOUND)
async def addtask_get(request:Request,year,type,
                      current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]): 
    cookies = request.cookies
    response = requests.get(
            f"http://localhost:8003/request_addtask/{year}/{type}",cookies=cookies
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)

@leave.post("/request_addtask/{year}/{type}",tags=['Leave'],status_code=status.HTTP_302_FOUND)
async def addtask(request:Request,year,type,
                  current_user: Annotated[User, Security(get_current_user_from_token, scopes=["employee","manager"])]):
    form_method=await request.form() 
    cookies = request.cookies
    async with httpx.AsyncClient() as client:
        response =await   client.post(
            f"http://localhost:8003/request_addtask/{year}/{type}",
            data=form_method,
            cookies=cookies
        )
        if response.status_code == status.HTTP_302_FOUND:
            redirect_url = response.headers.get('Location')
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.raise_for_status()
    
    return HTMLResponse(content=response.text, status_code=response.status_code)
    


@leave.get("/annualleaveadmin_view/{type}",tags=['Leave'],status_code=status.HTTP_302_FOUND)
async def annualleaveadmin_view_get(request:Request,type,
                                    current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])]): 
    cookies = request.cookies
    response = requests.get(
            f"http://localhost:8003/annualleaveadmin_view/{type}",cookies=cookies
        )
    response.raise_for_status()
    return HTMLResponse(content=response.text, status_code=response.status_code)


@leave.post("/annualleaveadmin_view/{type}",tags=['leave'],status_code=status.HTTP_302_FOUND)
async def annualleaveadmin_view(request:Request,type,
                               current_user: Annotated[User, Security(get_current_user_from_token, scopes=["manager"])]): 
    form_method=await request.form()
    cookies = request.cookies
    selecttiontasks=form_method.getlist('checkbox')
    form_data = dict(form_method)
    form_data['checkbox'] = selecttiontasks
    async with httpx.AsyncClient() as client:
        response =await   client.post(
            f"http://localhost:8003/annualleaveadmin_view/{type}",
            data=form_data,
            cookies=cookies
        )
        if response.status_code == status.HTTP_302_FOUND:
            redirect_url = response.headers.get('Location')
            return RedirectResponse(url=redirect_url, status_code=status.HTTP_302_FOUND)
        response.raise_for_status()
    
    return HTMLResponse(content=response.text, status_code=response.status_code)
    

