from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Bitacora(SQLModel, table=True):
    __tablename__ = "bitacoras"  # For User model
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int
    usuario_id: int
    accion: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)