import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter

from models import User, UserBase
from repositories import get_conn
from repositories.users import get_user_by_name

router = APIRouter(prefix="/login", tags=["login"])

load_dotenv()

TOKEN_EXPIRATION = 360
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


@router.post("/")
async def get_task(user: UserBase):
    conn = get_conn()
    task = get_user_by_name(conn, user.name.upper())
    conn.close()

    if (not task):
        return {"erro": f"Usuário {user.name} não encontrado"}

    full_user = User(
        id=task[0],
        name=task[1],
        password=task[2],
        role=task[3]
    )

    token_payload = {
        "sub": str(full_user.id),
        "name": full_user.name,
        "role": full_user.role,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION)
    }

    token = jwt.encode(token_payload, SECRET_KEY, ALGORITHM)

    return {"token": token}
