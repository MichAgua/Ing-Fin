from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from app.routers.auth import get_current_user
from datetime import datetime

router = APIRouter()

@router.post("/")
def crear_pedido(pedido: Pedido, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if user['role'] != 'ventas' and user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="No autorizado para crear pedidos")

    pedido.usuario_id = user['user_id']
    session.add(pedido)
    session.commit()
    session.refresh(pedido)

    bitacora = Bitacora(pedido_id=pedido.id, usuario_id=pedido.usuario_id, accion="Pedido creado")
    session.add(bitacora)
    session.commit()

    return pedido

@router.get("/")
def listar_pedidos(session: Session = Depends(get_session), user=Depends(get_current_user)):
    if user['role'] == 'admin':
        return session.exec(select(Pedido)).all()
    return session.exec(select(Pedido).where(Pedido.usuario_id == user['user_id'])).all()