from typing import Any, Optional

from fastapi import APIRouter, Depends, Response,Request
import models
import schemas
from libs.dependencies import Utils, UtilsObject

router = APIRouter()

@router.get('/')
async def index():
    return {
        "name":"jacker",
        "txet":"If you see this, you have been authenticated."
    }

from pydantic import BaseModel, validator


class UserBase(BaseModel):
    name: str
    txet: Optional[str] = ''


@router.post('/dataset1/protected')
async def auth_test(request:Request,response: Response,user :UserBase):
    from libs.snowflakeAlgorithm import IdWorker
    worker = IdWorker(1, 2, 0)
    request.session.update({'userId':user.name})
    request.session.update({'username':user.txet})
    request.session.update({'is_login':True})
    request.session.update({'datakey':worker.get_id()})
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {
        "name":user.name,
        "txet":user.txet
    }

