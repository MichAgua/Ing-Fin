from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Pedido(SQLModel, table=True):
    __tablename__ = "pedidos"
    __table_args__ = {"extend_existing": True}

    id: Optional[int] = Field(default=None, primary_key=True)
    cliente: str
    direccion: Optional[str]
    es_muestra: Optional[bool] = Field(default=False)
    prenda: Optional[str]  # camisa, pantalon, chamarra, chaleco
    tipo_tela: Optional[str]
    color: Optional[str]
    talla: Optional[str]
    cantidad: Optional[int]
    costo_estimado: Optional[float]
    explosion_materiales: Optional[str]  # descripción libre o JSON
    fecha_entrega: Optional[datetime]
    fecha: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default="pendiente")
    usuario_id: int