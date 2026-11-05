from typing import Optional, TYPE_CHECKING
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from app.models.user_models import User

class OrderBase(SQLModel):
    name: str = Field(index=True)  # <-- Nome do produto/item solicitado no pedido
    description: Optional[str] = Field(default=None) # Descrição opcional ou detalhes extras
    total_value: float
    status: str = Field(default="pending")

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: Optional[int] = Field(default=None)
    created_at: datetime
    user_id: int

class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    user_id: int = Field(foreign_key="user.id")
    
    # Relacionamento inverso com a tabela de usuários
    user: Optional["User"] = Relationship(back_populates="orders")