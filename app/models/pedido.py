from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: str
    direccion: str
    es_muestra: str
    prenda: str
    tipo_tela: str
    color: str
    talla: str
    cantidad: int
    costo_estimado: float
    explosion_materiales: str
    fecha_entrega: datetime
    fecha: datetime
    status: str = Field(default="pendiente")
    boton: Optional[str] = None
    cierre: Optional[str] = None
    estampado: Optional[str] = None
    bordado: Optional[str] = None
