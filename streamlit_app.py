import streamlit as st
from sqlmodel import Session, select
from app.database import engine
from app.models.user import User
from app.models.pedido import Pedido
from app.models.bitacora import Bitacora
from passlib.hash import bcrypt
from datetime import datetime

st.set_page_config(page_title="Sistema de Uniformes", layout="wide")
st.title("📋 Sistema de Uniformes")

if "user" not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.header("🔐 Login / Registro")
    tab = st.radio("Selecciona", ["Iniciar sesión", "Registrar usuario"])
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if tab == "Registrar usuario":
        full_name = st.text_input("Nombre completo")
        role = st.selectbox("Rol", ["ventas", "almacen", "admin"])
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
    selected = st.sidebar.radio("Módulo", ["📦 Pedidos", "📚 Bitácora"])

    if selected == "📦 Pedidos":
        st.header("📦 Gestión de Pedidos")
        with Session(engine) as session:
            if st.session_state.user.role in ["ventas", "admin"]:
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
            if st.session_state.user.role == "admin":
                pedidos = session.exec(select(Pedido)).all()
            else:
                pedidos = session