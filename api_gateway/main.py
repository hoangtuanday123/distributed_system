

from fastapi import APIRouter,Request,status,Response,Depends,FastAPI,Security
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse

from typing import Dict

from typing import Annotated
from fastapi.security import  OAuth2PasswordRequestForm
from datetime import datetime
import requests
from authentication.view import auth
from timesheet.views import timesheet
from leave.views import leave
app = FastAPI(
    title='api_gateway', openapi_url='/openapi.json', docs_url='/docs',
    description='api_gateway'
)
app.include_router(auth)
app.include_router(timesheet)
app.include_router(leave)