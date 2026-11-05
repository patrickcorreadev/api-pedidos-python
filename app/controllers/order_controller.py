from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List

from app.models.order_models import Order, OrderCreate

class OrderController:
    
    @staticmethod
    def index(session: Session) -> List[Order]:
        """Lista todos os pedidos (GET /orders)"""
        statement = select(Order)
        orders = session.exec(statement).all()
        return orders

    @staticmethod
    def store(order_in: OrderCreate, user_id: int, session: Session) -> Order:
        """Salva um novo pedido vinculado a um usuário (POST /orders)"""
        # Cria a instância da tabela de pedidos injetando o id do usuário dono
        db_order = Order(
            name=order_in.name,
            description=order_in.description,
            total_value=order_in.total_value,
            status=order_in.status,
            user_id=user_id
        )
        
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order

    @staticmethod
    def show(order_id: int, session: Session) -> Order:
        """Exibe um pedido específico pelo ID (GET /orders/{id})"""
        db_order = session.get(Order, order_id)
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado."
            )
        return db_order

    @staticmethod
    def update(order_id: int, order_in: OrderCreate, session: Session) -> Order:
        """Atualiza um pedido existente (PUT /orders/{id})"""
        db_order = session.get(Order, order_id)
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado."
            )
            
        # Atualiza dinamicamente os campos permitidos
        db_order.name = order_in.name
        db_order.description = order_in.description
        db_order.total_value = order_in.total_value
        db_order.status = order_in.status
            
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
        return db_order

    @staticmethod
    def destroy(order_id: int, session: Session) -> dict:
        """Remove um pedido do banco (DELETE /orders/{id})"""
        db_order = session.get(Order, order_id)
        if not db_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Pedido não encontrado."
            )
        
        session.delete(db_order)
        session.commit()
        return {"detail": "Pedido removido com sucesso."}