from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: str
    direccion: str
    es_muestra: Optional[bool] = False
    prenda: Optional[str] = None
    tipo_tela: Optional[str] = None
    color: Optional[str] = None
    talla: Optional[str] = None
    cantidad: Optional[int] = None
    costo_estimado: Optional[float] = None
    explosion_materiales: Optional[str] = None
    fecha_entrega: Optional[datetime] = None
    usuario_id: Optional[int] = None
    fecha: Optional[datetime] = None
    status: Optional[str] = "pendiente"
    boton: Optional[str] = None
    cierre: Optional[str] = None
    estampado: Optional[str] = None
    bordado: Optional[str] = None