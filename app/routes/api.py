from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from typing import List

# Imports da estrutura do projeto
from app.db.database import get_session
from app.controllers.user_controller import UserController
from app.controllers.order_controller import OrderController
from app.controllers.auth_controller import AuthController, decode_access_token
from app.models.user_models import User, UserCreate, UserResponse
from app.models.order_models import Order, OrderCreate, OrderResponse

router = APIRouter()

# Configura o FastAPI para habilitar o cadeado de autenticação (OAuth2 Bearer) no Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    """Dependência para proteger as rotas: valida o token JWT e retorna o usuário atual."""
    try:
        payload = decode_access_token(token)
        user_id = int(payload.get("sub"))
    except (ValueError, Exception):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado.")
    return user

# ==============================================================================
# ROTA DE AUTENTICAÇÃO (LOGIN)
# ==============================================================================

@router.post("/auth/login", status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Realiza o login e gera o token JWT."""
    return AuthController.login(email=form_data.username, password=form_data.password, session=session)

# ==============================================================================
# ROTAS DE USUÁRIOS (Equivalente ao Route::apiResource('users'))
# ==============================================================================

@router.get("/users", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
def index_users(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Lista todos os usuários (Protegido)"""
    return UserController.index(session)

@router.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def store_user(user_in: UserCreate, session: Session = Depends(get_session)):
    """Salva um novo usuário (Público - Sem cadeado para permitir cadastro)"""
    return UserController.store(user_in, session)

@router.get("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def show_user(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Exibe um usuário específico (Protegido)"""
    return UserController.show(id, session)

@router.put("/users/{id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(id: int, user_in: UserCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Atualiza um usuário existente (Protegido)"""
    return UserController.update(id, user_in, session)

@router.delete("/users/{id}", status_code=status.HTTP_200_OK)
def destroy_user(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Remove um usuário do banco (Protegido)"""
    return UserController.destroy(id, session)


# ==============================================================================
# ROTAS DE PEDIDOS (Equivalente ao Route::apiResource('orders'))
# ==============================================================================

@router.get("/orders", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
def index_orders(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Lista todos os pedidos (Protegido)"""
    return OrderController.index(session)

@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def store_order(order_in: OrderCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Cria um pedido vinculado ao ID do usuário do Token (Protegido)"""
    return OrderController.store(order_in, current_user.id, session)

@router.get("/orders/{id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def show_order(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Exibe um pedido específico (Protegido)"""
    return OrderController.show(id, session)

@router.put("/orders/{id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
def update_order(id: int, order_in: OrderCreate, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Atualiza um pedido existente (Protegido)"""
    return OrderController.update(id, order_in, session)

@router.delete("/orders/{id}", status_code=status.HTTP_200_OK)
def destroy_order(id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    """Remove um pedido do banco (Protegido)"""
    return OrderController.destroy(id, session)