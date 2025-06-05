from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime, date

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: str
    direccion: Optional[str] = None
    es_muestra: Optional[bool] = False
    prenda: Optional[str] = None
    tipo_tela: Optional[str] = None
    color: Optional[str] = None
    talla: Optional[str] = None
    cantidad: Optional[int] = 1
    costo_estimado: Optional[float] = 0.0
    explosion_materiales: Optional[str] = None
    fecha_entrega: Optional[date] = None
    usuario_id: Optional[int] = Field(default=None, foreign_key="users.id")
    fecha: datetime
    status: str = "pendiente"
   