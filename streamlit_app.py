import streamlit as st
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from app.models.cotizacion import Cotizacion  
from passlib.hash import bcrypt
from datetime import datetime
import pandas as pd

st.set_page_config(page_title="Sistema de Uniformes", layout="wide")
st.title("📋 Sistema de Uniformes")

st.title("Inicio de sesión")
username = st.text_input("Usuario")
password = st.text_input("Contraseña", type="password")

with Session(engine) as session:
    user = session.exec(select(User).where(User.username == username)).first()

    if user and bcrypt.verify(password, user.hashed_password):
        st.success(f"Bienvenido, {user.full_name} ({user.role})")

if "user" not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.header("🔐 Login / Registro")
    tab = st.radio("Selecciona", ["Iniciar sesión", "Registrar usuario"])
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if tab == "Registrar usuario":
        full_name = st.text_input("Nombre completo")
        role = st.selectbox("Rol", ["ventas", "almacen", "contabilidad", "rh", "admin"])
        if st.button("Registrar"):
            with Session(engine) as session:
                existing = session.exec(select(User).where(User.username == username)).first()
                if existing:
                    st.warning("Ese usuario ya existe.")
                else:
                    new_user = User(
                        username=username,
                        full_name=full_name,
                        role=role,
                        hashed_password=bcrypt.hash(password)
                    )
                    session.add(new_user)
                    session.commit()
                    st.success("Usuario registrado correctamente.")
    else:
        if st.button("Iniciar sesión"):
            with Session(engine) as session:
                user = session.exec(select(User).where(User.username == username)).first()
                if not user or not bcrypt.verify(password, user.hashed_password):
                    st.error("Credenciales incorrectas")
                else:
                    st.session_state.user = user
                    st.success(f"Bienvenido, {user.full_name} ({user.role})")

if st.session_state.user:
    st.sidebar.success(f"Sesión iniciada: {st.session_state.user.full_name}")
    role = st.session_state.user.role
    allowed_modules = ["📦 Pedidos", "📚 Bitácora"]
    if role == "admin":
        allowed_modules.append("📊 Reportes")

    selected = st.sidebar.radio("Módulo", allowed_modules)

    if selected == "📦 Pedidos":
        st.header("📦 Gestión de Pedidos")
        with Session(engine) as session:
            if role in ["ventas", "admin"]:
                st.subheader("Crear nuevo pedido")
                cliente = st.text_input("Nombre del cliente")
                if st.button("Crear pedido") and cliente:
                    nuevo = Pedido(
                        cliente=cliente,
                        usuario_id=st.session_state.user.id,
                        fecha=datetime.utcnow(),
                        status="pendiente"
                    )
                    session.add(nuevo)
                    session.commit()
                    bit = Bitacora(
                        pedido_id=nuevo.id,
                        usuario_id=nuevo.usuario_id,
                        accion="Pedido creado",
                        timestamp=datetime.utcnow()
                    )
                    session.add(bit)
                    session.commit()
                    st.success("Pedido creado")

            st.subheader("Lista de pedidos")
            if role == "admin":
                pedidos = session.exec(select(Pedido)).all()
            else:
                pedidos = session.exec(select(Pedido).where(Pedido.usuario_id == st.session_state.user.id)).all()

            for p in pedidos:
                cols = st.columns([4, 2, 2])
                with cols[0]:
                    st.write(f"📌 Pedido #{p.id} — Cliente: {p.cliente} — Fecha: {p.fecha.strftime('%Y-%m-%d')} — Estado: {p.status}")
                if role == "admin":
                    with cols[1]:
                        if st.button(f"✅ Aprobar #{p.id}"):
                            p.status = "aprobado"
                            session.add(p)
                            session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido aprobado", timestamp=datetime.utcnow()))
                            session.commit()
                            st.rerun()
                    with cols[2]:
                        if st.button(f"❌ Rechazar #{p.id}"):
                            p.status = "rechazado"
                            session.add(p)
                            session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido rechazado", timestamp=datetime.utcnow()))
                            session.commit()
                            st.rerun()

    elif selected == "📚 Bitácora":
        st.header("📚 Historial de Acciones")
        with Session(engine) as session:
            if role == "admin":
                bitacora = session.exec(select(Bitacora)).all()
            else:
                bitacora = session.exec(select(Bitacora).where(Bitacora.usuario_id == st.session_state.user.id)).all()
            for b in bitacora:
                st.write(f"🕒 {b.timestamp.strftime('%Y-%m-%d %H:%M:%S')} — Pedido #{b.pedido_id} — Acción: {b.accion}")

    elif selected == "📊 Reportes":
        st.header("📊 Dashboard de Reportes")
        with Session(engine) as session:
            pedidos = session.exec(select(Pedido)).all()
            if pedidos:
                df = pd.DataFrame([{
                    "ID": p.id,
                    "Cliente": p.cliente,
                    "Fecha": p.fecha.date(),
                    "Status": p.status,
                    "Usuario": p.usuario_id
                } for p in pedidos])

                st.subheader("Pedidos por estado")
                st.bar_chart(df["Status"].value_counts())

                st.subheader("Pedidos por día")
                st.line_chart(df.groupby("Fecha").size())

                st.subheader("Pedidos por usuario")
                st.bar_chart(df.groupby("Usuario").size())
            else:
                st.info("No hay pedidos aún para mostrar.")
