from sqlmodel import SQLModel, Session, create_engine
from app.models.user import User
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from passlib.hash import bcrypt
from datetime import datetime

engine = create_engine("sqlite:///./uniformes.db")

SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    # Usuarios iniciales
    users = [
        User(username="admin", full_name="Administrador", role="admin", hashed_password=bcrypt.hash("admin123")),
        User(username="ventas1", full_name="Juan Ventas", role="ventas", hashed_password=bcrypt.hash("ventas123")),
        User(username="almacen1", full_name="Ana Almacén", role="almacen", hashed_password=bcrypt.hash("almacen123"))
    ]
    session.add_all(users)
    session.commit()

    # Pedidos iniciales
    pedidos = [
        Pedido(cliente="Coca Cola", usuario_id=2, status="pendiente"),
        Pedido(cliente="Oxxo", usuario_id=2, status="pendiente")
    ]
    session.add_all(pedidos)
    session.commit()

    # Bitácora
    bitacora = [
        Bitacora(pedido_id=1, usuario_id=2, accion="Pedido creado", timestamp=datetime.utcnow()),
        Bitacora(pedido_id=2, usuario_id=2, accion="Pedido creado", timestamp=datetime.utcnow())
    ]
    session.add_all(bitacora)
    session.commit()

print("✅ Base de datos creada con usuarios y pedidos de prueba.")