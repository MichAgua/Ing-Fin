from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Bitacora(SQLModel, table=True):
    __tablename__ = "users"  # For User model
    
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int
    usuario_id: int
    accion: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)