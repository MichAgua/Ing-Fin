from sqlmodel import SQLModel, Session, create_engine
from app.models.user import User
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from passlib.hash import bcrypt
from datetime import datetime

engine = create_engine("sqlite:///./uniformes.db")
SQLModel.metadata.create_all(engine)

with Session(engine) as session:
    # Crear usuario principal
    admin_user = User(username="admin", full_name="Administrador", role="admin", hashed_password=bcrypt.hash("admin123"))
    session.add(admin_user)
    session.commit()

    # Crear pedidos de prueba
    pedidos = [
        Pedido(cliente="Coca Cola", direccion="Av. Industria 123", usuario_id=admin_user.id, status="pendiente"),
        Pedido(cliente="SIAPA", direccion="Calle Agua 456", usuario_id=admin_user.id, status="pendiente"),
        Pedido(cliente="Akron", direccion="Boulevard Petróleo 789", usuario_id=admin_user.id, status="pendiente"),
    ]
    session.add_all(pedidos)
    session.commit()

    # Crear bitácora para cada pedido
    for pedido in pedidos:
        bit = Bitacora(pedido_id=pedido.id, usuario_id=admin_user.id, accion="Pedido creado automáticamente", timestamp=datetime.utcnow())
        session.add(bit)

    session.commit()

print("✅ Base de datos creada con pedidos de prueba (Coca Cola, SIAPA, Akron).")