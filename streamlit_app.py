import streamlit as st
from streamlit.components.v1 import html
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

# Global CSS styles
st.markdown("""
    <style>
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Segoe UI', sans-serif;
    }
    .stButton>button {
        border-radius: 6px;
        border: none;
        background-color: #0d6efd;
        color: white;
        padding: 0.4rem 1rem;
        font-size: 1rem;
    }
    .stButton>button:hover {
        background-color: #084298;
    }
    </style>
""", unsafe_allow_html=True)

# Sleek welcome section
with st.container():
    st.markdown("<h2 style='color: #333;'>Alfa Uniformes - Sistema General</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666;'>De acuerdo al area en el que trabajes, podras administrar pedidos, crear cotizaciónes, modificar ordenes y trabajar de manera eficiente.</p>", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.markdown("<h3 style='margin-bottom: 0.5rem;'>Login / Registro</h3>", unsafe_allow_html=True)
    tab = st.radio("Selecciona", ["Iniciar sesión", "Registrar usuario"])
    username = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if tab == "Registrar usuario":
        full_name = st.text_input("Nombre completo")
        role = st.selectbox("Rol", ["ventas", "almacen", "contabilidad", "rh", "admin"])
        if st.button("Registrar", use_container_width=True):
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
        if st.button("Iniciar sesión", use_container_width=True):
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
    allowed_modules = [" Inicio", " Mi Perfil", " Pedidos", " Bitácora"]
    if role == "admin":
        allowed_modules.append(" Reportes")

    selected = st.sidebar.radio("Módulo", allowed_modules)

    if selected == "🏠 Inicio":
        with stylable_container("section-header", css_styles="margin-bottom: 1rem; padding: 1rem; background-color: #f1f3f5; border-radius: 6px;"):
            st.markdown("### 🏠 Bienvenido")
        st.write("Selecciona una opción del menú para comenzar.")

    elif selected == "👤 Mi Perfil":
        with stylable_container("section-header", css_styles="margin-bottom: 1rem; padding: 1rem; background-color: #f1f3f5; border-radius: 6px;"):
            st.markdown("###  Mi Perfil")
        st.write({
            "ID": st.session_state.user.id,
            "Usuario": st.session_state.user.username,
            "Nombre completo": st.session_state.user.full_name,
            "Rol": st.session_state.user.role,
        })

    elif selected == " Pedidos":
        with stylable_container("section-header", css_styles="margin-bottom: 1rem; padding: 1rem; background-color: #f1f3f5; border-radius: 6px;"):
            st.markdown("###  Gestión de Pedidos")
        with Session(engine) as session:
            if role in ["ventas", "admin"]:
                st.subheader("Crear nuevo pedido")
                cliente = st.text_input("Nombre del cliente")
                if st.button("Crear pedido", use_container_width=True) and cliente:
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
                    st.write(f" Pedido #{p.id} — Cliente: {p.cliente} — Fecha: {p.fecha.strftime('%Y-%m-%d')} — Estado: {p.status}")
                if role == "admin":
                    with cols[1]:
                        if st.button(f" Aprobar #{p.id}", use_container_width=True):
                            p.status = "aprobado"
                            session.add(p)
                            session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido aprobado", timestamp=datetime.utcnow()))
                            session.commit()
                            st.rerun()
                    with cols[2]:
                        if st.button(f" Rechazar #{p.id}", use_container_width=True):
                            p.status = "rechazado"
                            session.add(p)
                            session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido rechazado", timestamp=datetime.utcnow()))
                            session.commit()
                            st.rerun()

    elif selected == " Bitácora":
        with stylable_container("section-header", css_styles="margin-bottom: 1rem; padding: 1rem; background-color: #f1f3f5; border-radius: 6px;"):
            st.markdown("###  Historial de Acciones")
        with Session(engine) as session:
            if role == "admin":
                bitacora = session.exec(select(Bitacora)).all()
            else:
                bitacora = session.exec(select(Bitacora).where(Bitacora.usuario_id == st.session_state.user.id)).all()
            for b in bitacora:
                st.write(f" {b.timestamp.strftime('%Y-%m-%d %H:%M:%S')} — Pedido #{b.pedido_id} — Acción: {b.accion}")

    elif selected == " Reportes":
        with stylable_container("section-header", css_styles="margin-bottom: 1rem; padding: 1rem; background-color: #f1f3f5; border-radius: 6px;"):
            st.markdown("### Dashboard de Reportes")
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
