from sqlmodel import SQLModel
from app.database import engine
from app.models.user import User
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from app.models.cotizacion import Cotizacion

def crear_tablas():
    SQLModel.metadata.create_all(engine)
    print("✅ Tablas creadas correctamente.")

if __name__ == "__main__":
    crear_tablas()