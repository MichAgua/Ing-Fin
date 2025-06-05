from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

__tablename__ = "pedidos"

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: str
    direccion: str
    es_muestra: bool
    prenda: str
    tipo_tela: str
    color: str
    talla: str
    cantidad: int
    costo_estimado: float
    explosion_materiales: str
    fecha_entrega: datetime
    usuario_id: int
    fecha: datetime
    status: str = "pendiente"
    boton: Optional[str] = None
    cierre: Optional[str] = None
    estampado: Optional[str] = None
    bordado: Optional[str] = None
   