import os
from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from sqlmodel import Session, select
from fastapi import HTTPException, status

from app.models.user_models import User

# --- Seu código original mantido com sucesso ---
SECRET_KEY = os.getenv("SECRET_KEY", "SUA_CHAVE_SECRETISSIMA_AQUI_ALTERE_EM_PRODUCAO")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Gera o hash de uma senha em texto puro."""
    try:
        return pwd_context.hash(password)
    except Exception as e:
        raise RuntimeError("Erro ao gerar o hash da senha.") from e

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto puro corresponde ao hash fornecido."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Cria um token JWT de acesso seguro com tempo de expiração estruturado."""
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt
    except Exception as e:
        raise RuntimeError("Erro ao gerar o token de acesso.") from e

def decode_access_token(token: str) -> Dict[str, Any]:
    """Decodifica e valida um token JWT recebido pela API."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise ValueError("Token inválido ou expirado.") from e


# --- Nova classe inserida no final do arquivo para o apiResource ---
class AuthController:
    @staticmethod
    def login(email: str, password: str, session: Session) -> dict:
        """Verifica as credenciais e retorna o token JWT."""
        # Busca o usuário pelo e-mail
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        
        # Verifica se o usuário existe e se a senha bate com o hash
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha incorretos.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        # Cria o token de acesso com o ID e o E-mail dele
        token_data = {"sub": str(user.id), "email": user.email}
        access_token = create_access_token(data=token_data)
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {"id": user.id, "name": user.name, "email": user.email}
        }