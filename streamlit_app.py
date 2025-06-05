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
    st.markdown("<h2 style='color: #333; font-weight: 700;'>🛡️ Alfa Uniformes - Sistema General</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-weight: 500; margin-bottom: 1.5rem;'>De acuerdo al área en el que trabajes, podrás administrar pedidos, crear cotizaciones, modificar órdenes y trabajar de manera eficiente.</p>", unsafe_allow_html=True)

    # Improved Emoji rotation area in main page
    emoji_list = ["📦", "📄", "📋", "👷", "✂️", "🧾"]
    emoji_script = f"""
<script>
  let emojis = {emoji_list};
  let index = 0;
  function rotateEmoji() {{
    const el = document.getElementById("emoji-rotator");
    if (el) {{
      el.innerHTML = emojis[index % emojis.length];
      index++;
    }}
  }}
  setInterval(rotateEmoji, 8000); // Change every 8 seconds
  document.addEventListener("DOMContentLoaded", rotateEmoji);
</script>
"""

    st.markdown("""
<div style='text-align: center; margin-top: 3rem;'>
  <div id='emoji-rotator' style='font-size: 6rem;'>📦</div>
  <div style='color: #0d6efd; font-size: 1.8rem; font-weight: 700; margin-top: 1rem;'>
    Sistema seguro y eficiente para la gestión de uniformes.
  </div>
</div>
""", unsafe_allow_html=True)

    import streamlit.components.v1 as components
    components.html(emoji_script, height=0)

if "user" not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.markdown("<h3 style='margin-bottom: 0.5rem; font-weight: 700;'>Login / Registro</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns([2,1])
    with col1:
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
    allowed_modules = ["🏠 Inicio", "👤 Mi Perfil", "📦 Pedidos", "📝 Bitácora"]
    if role == "admin":
        allowed_modules.append("📊 Reportes")

    selected = st.sidebar.radio("Módulo", allowed_modules)

    if selected == "🏠 Inicio":
        with st.container():
            st.markdown("<h3 style='color: #333; font-weight: 700; margin-bottom: 0.5rem;'>🏠 Bienvenido</h3>", unsafe_allow_html=True)
            st.write("Selecciona una opción del menú para comenzar.")
        st.markdown("---")

    elif selected == "👤 Mi Perfil":
        with st.container():
            st.markdown("<h3 style='color: #333; font-weight: 700; margin-bottom: 0.5rem;'>👤 Mi Perfil</h3>", unsafe_allow_html=True)
            profile_data = {
                "Campo": ["ID", "Usuario", "Nombre completo", "Rol"],
                "Valor": [
                    st.session_state.user.id,
                    st.session_state.user.username,
                    st.session_state.user.full_name,
                    st.session_state.user.role,
                ]
            }
            df_profile = pd.DataFrame(profile_data)
            st.table(df_profile)
        st.markdown("---")

    elif selected == "📦 Pedidos":
        with st.container():
            st.markdown("<h3 style='color: #333; font-weight: 700; margin-bottom: 1rem;'>📦 Gestión de Pedidos</h3>", unsafe_allow_html=True)
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
                    st.markdown("---")

                st.subheader("Lista de pedidos")
                if role == "admin":
                    pedidos = session.exec(select(Pedido)).all()
                else:
                    pedidos = session.exec(select(Pedido).where(Pedido.usuario_id == st.session_state.user.id)).all()

                for p in pedidos:
                    cols = st.columns([4, 2, 2])
                    with cols[0]:
                        status_color = {
                            "aprobado": "#198754",
                            "pendiente": "#0d6efd",
                            "rechazado": "#dc3545"
                        }.get(p.status, "#6c757d")
                        st.markdown(f"**Pedido #{p.id}** — Cliente: {p.cliente} — Fecha: {p.fecha.strftime('%Y-%m-%d')} — Estado: <span style='color:{status_color}; font-weight:600;'>{p.status.capitalize()}</span>", unsafe_allow_html=True)
                    if role == "admin":
                        with cols[1]:
                            if st.button(f" Aprobar #{p.id}", use_container_width=True):
                                p.status = "aprobado"
                                session.add(p)
                                session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido aprobado", timestamp=datetime.utcnow()))
                                session.commit()
                                st.experimental_rerun()
                        with cols[2]:
                            if st.button(f" Rechazar #{p.id}", use_container_width=True):
                                p.status = "rechazado"
                                session.add(p)
                                session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido rechazado", timestamp=datetime.utcnow()))
                                session.commit()
                                st.experimental_rerun()
        st.markdown("---")

    elif selected == "📝 Bitácora":
        with st.container():
            st.markdown("<h3 style='color: #333; font-weight: 700; margin-bottom: 1rem;'>📝 Historial de Acciones</h3>", unsafe_allow_html=True)
            with Session(engine) as session:
                if role == "admin":
                    bitacora = session.exec(select(Bitacora)).all()
                else:
                    bitacora = session.exec(select(Bitacora).where(Bitacora.usuario_id == st.session_state.user.id)).all()
                for b in bitacora:
                    st.markdown(f"📅 {b.timestamp.strftime('%Y-%m-%d %H:%M:%S')} — Pedido #{b.pedido_id} — Acción: {b.accion}")
        st.markdown("---")

    elif selected == "📊 Reportes":
        with st.container():
            st.markdown("<h3 style='color: #333; font-weight: 700; margin-bottom: 1rem; text-align:center;'>📊 Dashboard de Reportes</h3>", unsafe_allow_html=True)
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

                    with st.expander("Pedidos por estado"):
                        st.markdown("<p style='text-align:center; font-weight:600;'>Distribución de pedidos según su estado actual.</p>", unsafe_allow_html=True)
                        st.bar_chart(df["Status"].value_counts())

                    with st.expander("Pedidos por día"):
                        st.markdown("<p style='text-align:center; font-weight:600;'>Número de pedidos creados diariamente.</p>", unsafe_allow_html=True)
                        st.line_chart(df.groupby("Fecha").size())

                    with st.expander("Pedidos por usuario"):
                        st.markdown("<p style='text-align:center; font-weight:600;'>Cantidad de pedidos por usuario.</p>", unsafe_allow_html=True)
                        st.bar_chart(df.groupby("Usuario").size())
                else:
                    st.info("No hay pedidos aún para mostrar.")
        st.markdown("---")
