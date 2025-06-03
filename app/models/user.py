import streamlit as st
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from passlib.hash import bcrypt
from datetime import datetime
import pandas as pd

# Inicio de sesión
st.title("Inicio de sesión")
username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

with Session(engine) as session:
    user = session.exec(select(User).where(User.username == username)).first()

    if user and bcrypt.verify(password, user.hashed_password):
        st.success(f"Bienvenido, {user.full_name} ({user.role})")

        # Paneles específicos por rol
        if user.role == "admin":
            st.subheader("Panel Admin")
            st.write("Acceso completo al sistema.")
        elif user.role == "ventas":
            st.subheader("Panel Ventas")
            st.write("Pedidos asignados, estado y creación.")
        elif user.role == "almacen":
            st.subheader("Panel Almacén")
            st.write("Pedidos pendientes por surtir.")
        elif user.role == "contabilidad":
            st.subheader("Panel Contabilidad")
            st.write("Pedidos facturados y pendientes de facturar.")
        elif user.role == "rh":
            st.subheader("Panel Recursos Humanos")
            st.write("Información de responsables y roles.")
        else:
            st.warning("Rol no reconocido")

        # Dashboard para admin
        if user.role == "admin":
            st.title("📊 Dashboard General")

            pedidos = session.exec(select(Pedido)).all()
            pedidos_df = pd.DataFrame([p.dict() for p in pedidos])

            if not pedidos_df.empty:
                pedidos_df["fecha"] = pd.to_datetime(pedidos_df["fecha"])
                st.line_chart(pedidos_df.groupby(pedidos_df["fecha"].dt.date).size())
                st.bar_chart(pedidos_df["status"].value_counts())
                st.dataframe(pedidos_df)
            else:
                st.info("No hay pedidos registrados todavía.")
    elif username and password:
        st.error("Usuario o contraseña incorrectos")