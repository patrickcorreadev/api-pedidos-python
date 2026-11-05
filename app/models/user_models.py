from typing import Optional, List, TYPE_CHECKING
from sqlmodel import SQLModel, Field, Relationship

# O TYPE_CHECKING é True apenas para o VS Code / Linters. 
# Em tempo de execução ele é False, evitando o erro de importação cíclica.
if TYPE_CHECKING:
    from app.models.order_models import Order

class UserBase(SQLModel):
    name: str
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: Optional[int] = Field(default=None)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    # O VS Code agora reconhecerá a classe Order perfeitamente
    orders: List["Order"] = Relationship(back_populates="user")