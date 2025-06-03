from fastapi import FastAPI
from app.routers import auth, pedidos, users, cotizaciones
from app.database import create_db_and_tables

app = FastAPI(title="Sistema de Uniformes")

create_db_and_tables()

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(pedidos.router, prefix="/pedidos", tags=["Pedidos"])
app.include_router(cotizaciones.router, prefix="/cotizaciones", tags=["Cotizaciones"])