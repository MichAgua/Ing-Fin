from sqlmodel import SQLModel, Session, create_engine, select
from app.models.pedido import Pedido
from datetime import datetime, date

engine = create_engine("sqlite:///app/database.db")

pedidos = [
    Pedido(
        cliente="Coca Cola",
        direccion="Av. Industria 123, Guadalajara, Jalisco",
        es_muestra=False,
        prenda="Camisa",
        tipo_tela="Mezclilla",
        color="Rojo",
        talla="M",
        cantidad=50,
        costo_estimado=5000.0,
        explosion_materiales="Botones metálicos, bordado frontal, etiqueta interna",
        fecha_entrega=date(2025, 7, 1),
        fecha=datetime.now(),
        status="pendiente"
    ),
    Pedido(
        cliente="SIAPA",
        direccion="Calle Agua 456, Zapopan, Jalisco",
        es_muestra=True,
        prenda="Chamarra",
        tipo_tela="Kakhi",
        color="Azul",
        talla="L",
        cantidad=10,
        costo_estimado=3000.0,
        explosion_materiales="Cierre grueso, logo bordado, forro térmico",
        fecha_entrega=date(2025, 6, 20),
        fecha=datetime.now(),
        status="pendiente"
    ),
    Pedido(
        cliente="Akron",
        direccion="Blvd. Aceite 789, Tlaquepaque, Jalisco",
        es_muestra=False,
        prenda="Pantalón",
        tipo_tela="Gabardina",
        color="Negro",
        talla="32",
        cantidad=30,
        costo_estimado=6000.0,
        explosion_materiales="Cierre de metal, botón reforzado, etiquetas interiores",
        fecha_entrega=date(2025, 6, 28),
        fecha=datetime.now(),
        status="pendiente"
    )
]

with Session(engine) as session:
    for pedido in pedidos:
        session.add(pedido)
    session.commit()
    print("✅ Pedidos insertados exitosamente.")