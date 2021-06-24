from typing import Any, Optional

from fastapi import APIRouter, Depends, HTTPException

import models
import schemas
from libs.dependencies import Utils, UtilsObject

router = APIRouter()

@router.get('/')
async def index():
    return "If you see this, you have been authenticated."


@router.get('/dataset1/protected')
async def auth_test():
    return "You must be alice to see this."