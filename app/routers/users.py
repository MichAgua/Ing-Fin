from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from passlib.hash import bcrypt

router = APIRouter()

@router.post("/")
def create_user(user: User, session: Session = Depends(get_session)):
    user.hashed_password = bcrypt.hash(user.hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@router.get("/")
def list_users(session: Session = Depends(get_session)):
    users = session.exec(select(User)).all()
    return users