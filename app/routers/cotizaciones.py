from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.cotizacion import Cotizacion
from app.routers.auth import get_current_user

router = APIRouter()

@router.post("/")
def crear_cotizacion(cot: Cotizacion, session: Session = Depends(get_session), user=Depends(get_current_user)):
    if user['role'] != 'ventas' and user['role'] != 'admin':
        raise HTTPException(status_code=403, detail="No autorizado para crear cotizaciones")

    cot.total = cot.precio_unitario * cot.cantidad
    session.add(cot)
    session.commit()
    session.refresh(cot)
    return cot

@router.get("/")
def listar_cotizaciones(session: Session = Depends(get_session), user=Depends(get_current_user)):
    if user['role'] == 'admin':
        return session.exec(select(Cotizacion)).all()
    return session.exec(select(Cotizacion).where(Cotizacion.pedido_id.is_not(None))).all()