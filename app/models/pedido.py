from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: str
    fecha: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pendiente")
    usuario_id: int