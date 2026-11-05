from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List

from app.models.user_models import User, UserCreate
from .auth_controller import get_password_hash

class UserController:
    
    @staticmethod
    def index(session: Session) -> List[User]:
        """Lista todos os usuários (GET /users)"""
        statement = select(User)
        users = session.exec(statement).all()
        return users

    @staticmethod
    def store(user_in: UserCreate, session: Session) -> User:
        """Salva um novo usuário com senha criptografada (POST /users)"""
        # Verifica se o e-mail já está cadastrado
        statement = select(User).where(User.email == user_in.email)
        existing_user = session.exec(statement).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Este e-mail já está cadastrado no sistema."
            )
        
        # Criptografa a senha usando o seu auth.py
        hashed_pwd = get_password_hash(user_in.password)
        
        # Cria a instância da tabela omitindo a senha em texto puro
        db_user = User(
            name=user_in.name,
            email=user_in.email,
            is_active=user_in.is_active,
            hashed_password=hashed_pwd
        )
        
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def show(user_id: int, session: Session) -> User:
        """Exibe um usuário específico pelo ID (GET /users/{id})"""
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        return db_user

    @staticmethod
    def update(user_id: int, user_in: UserCreate, session: Session) -> User:
        """Atualiza um usuário existente (PUT /users/{id})"""
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
            
        # Atualiza os campos básicos
        db_user.name = user_in.name
        db_user.email = user_in.email
        db_user.is_active = user_in.is_active
        
        # Se uma nova senha foi enviada, atualiza o hash
        if user_in.password:
            db_user.hashed_password = get_password_hash(user_in.password)
            
        session.add(db_user)
        session.commit()
        session.refresh(db_user)
        return db_user

    @staticmethod
    def destroy(user_id: int, session: Session) -> dict:
        """Remove um usuário do banco (DELETE /users/{id})"""
        db_user = session.get(User, user_id)
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado."
            )
        
        session.delete(db_user)
        session.commit()
        return {"detail": "Usuário removido com sucesso."}