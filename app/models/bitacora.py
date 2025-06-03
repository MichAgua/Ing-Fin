from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Bitacora(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int
    usuario_id: int
    accion: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)