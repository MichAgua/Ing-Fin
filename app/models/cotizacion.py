from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Cotizacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    descripcion: str
    precio_unitario: float
    cantidad: int
    total: float
    fecha: datetime = Field(default_factory=datetime.utcnow)
    pedido_id: Optional[int] = None