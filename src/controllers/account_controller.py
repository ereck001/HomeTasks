import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from fastapi.responses import UJSONResponse

from authentication import hash_password, verify_password, verify_token
from models import User, UserBase
from repositories import get_conn
from repositories.users import add_user, get_user_by_name

router = APIRouter(prefix="/user", tags=["user"])

load_dotenv()

TOKEN_EXPIRATION = 360
ALGORITHM = os.getenv("ALGORITHM")
SECRET_KEY = os.getenv("SECRET_KEY")


@router.post("/login")
async def login(user: UserBase):
    conn = get_conn()
    stored_user = get_user_by_name(conn, user.name.lower())
    conn.close()

    if (not stored_user):
        return {"erro": f"Usuário {user.name} não encontrado"}

    full_user = User(
        id=stored_user[0],
        name=stored_user[1],
        password=stored_user[2],
        role=stored_user[3]
    )

    token_payload = {
        "sub": str(full_user.id),
        "name": full_user.name,
        "role": full_user.role,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRATION)
    }

    if (not verify_password(user.password, full_user.password)):
        return UJSONResponse({'Erro': 'Senha incorreta'}, 401)

    token = jwt.encode(token_payload, SECRET_KEY, ALGORITHM)

    return {"token": token}


@router.post("/add", dependencies=[Depends(verify_token)])
async def add(user: UserBase, token_data: dict = Depends(verify_token)):

    if token_data.get('role') != 1:
        return UJSONResponse({'Erro': 'O Usuário não é administrador'}, 401)

    if user.name.strip() == "":
        return UJSONResponse({'Erro': 'O nome é obrigatório'}, 400)
    conn = get_conn()
    user_name = add_user(conn, user.name.lower(), hash_password(user.password))
    conn.close()

    return {'Adicionado': user_name}
