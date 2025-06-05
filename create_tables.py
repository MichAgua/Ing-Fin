from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from app.models.cotizacion import Cotizacion

print("🔧 Creando tablas en la base de datos...")
SQLModel.metadata.create_all(engine)
print("✅ Tablas creadas correctamente.")