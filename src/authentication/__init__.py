import os

import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        # Decodificar o token
        payload = jwt.decode(token.strip(), SECRET_KEY, algorithms=[
                             ALGORITHM])  # type: ignore
        user_id: int = payload.get("sub")  # Extrair o 'sub' (id do usuário)
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido: usuário não encontrado",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # Retorna o payload decodificado (pode ser usado no endpoint)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
