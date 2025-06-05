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
    <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">
    <style>
    .stApp {
        background-color: #f5f7fa;
        font-family: 'Roboto', sans-serif;
    }
    h2, h3 {
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
    }
    p {
        font-size: 1.2rem;
        line-height: 1.6;
        color: #444;
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

# Sleek welcome section (only show if not logged in)
if st.session_state.get("user") is None:
    # Sleek welcome section
    with st.container():
        st.markdown("<h2 style='color: #333; font-weight: 700;'>🛡️ Alfa Uniformes - Sistema General</h2>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666; font-weight: 500; margin-bottom: 1.5rem;'>De acuerdo al área en el que trabajes, podrás administrar pedidos, crear cotizaciones, modificar órdenes y trabajar de manera eficiente.</p>", unsafe_allow_html=True)

        # Improved Emoji rotation area
        emoji_list = ["📦", "📄", "📋", "👷", "✂️", "🧾"]
        emoji_script = """
        <div style='text-align: center; margin-top: 3rem;'>
          <div id='emoji-rotator' style='font-size: 6rem;'>📦</div>
          <div style='color: #0d6efd; font-size: 1.8rem; font-weight: 700; margin-top: 1rem;'>
            Sistema seguro y eficiente para la gestión de uniformes.
          </div>
        </div>
        <script>
          const emojis = ["📦", "📄", "📋", "👷", "✂️", "🧾"];
          let idx = 0;
          setInterval(() => {
            const container = document.getElementById("emoji-rotator");
            if (container) {
              idx = (idx + 1) % emojis.length;
              container.innerHTML = emojis[idx];
            }
          }, 5000);
        </script>
        """
        st.markdown(emoji_script, unsafe_allow_html=True)

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
    # Botón para cerrar sesión
    st.sidebar.button("🔓 Cerrar sesión", on_click=lambda: st.session_state.pop("user"))
    role = st.session_state.user.role
    allowed_modules = ["🏠 Inicio", "👤 Mi Perfil", "📦 Pedidos", "📝 Bitácora"]
    if role == "admin":
        allowed_modules.append("📊 Reportes")

    selected = st.sidebar.radio("Módulo", allowed_modules)

    if selected == "🏠 Inicio":
        with st.container():
            st.markdown("""
                <div style='background: linear-gradient(to right, #e3f2fd, #fff); padding: 2rem; border-radius: 10px;'>
                    <h3 style='color: #0d47a1; font-weight: 800; font-size: 2.2rem; margin-bottom: 0.2rem;'>🏠 Bienvenido a Alfa Uniformes</h3>
                    <p style='font-size:1.3rem; color: #333;'>Selecciona el área con la que deseas trabajar:</p>
                </div>
            """, unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("👕 Ventas", key="ventas_btn", use_container_width=True):
                    st.session_state.selected_area = "ventas"
                    st.session_state.selected = "🏠 Inicio"
                    st.rerun()
            with col2:
                if st.button("📦 Almacén", key="almacen_btn", use_container_width=True):
                    st.session_state.selected_area = "almacen"
                    st.session_state.selected = "🏠 Inicio"
                    st.rerun()
            with col3:
                if st.button("🧾 Contabilidad", key="contabilidad_btn", use_container_width=True):
                    st.session_state.selected_area = "contabilidad"
                    st.session_state.selected = "🏠 Inicio"
                    st.rerun()

            col4, col5, col6 = st.columns(3)
            with col4:
                if st.button("👥 Recursos Humanos", key="rh_btn", use_container_width=True):
                    st.session_state.selected_area = "rh"
                    st.session_state.selected = "🏠 Inicio"
                    st.rerun()
            with col5:
                if st.button("🛠️ Admin", key="admin_btn", use_container_width=True):
                    st.session_state.selected_area = "admin"
                    st.session_state.selected = "🏠 Inicio"
                    st.rerun()
            with col6:
                if st.button("📦 Pedidos", key="pedidos_btn", use_container_width=True):
                    st.session_state.selected_area = "pedidos"
                    st.session_state.selected = "📦 Pedidos"
                    st.rerun()

            col7, col8 = st.columns(2)
            with col7:
                if st.button("📝 Bitácora", key="bitacora_btn", use_container_width=True):
                    st.session_state.selected_area = "bitacora"
                    st.session_state.selected = "📝 Bitácora"
                    st.rerun()
            with col8:
                if st.button("📊 Reportes", key="reportes_btn", use_container_width=True):
                    st.session_state.selected_area = "reportes"
                    st.session_state.selected = "📊 Reportes"
                    st.rerun()

            st.markdown("<hr style='margin-top: 2rem; margin-bottom: 1rem;'>", unsafe_allow_html=True)

    elif selected == "👤 Mi Perfil":
        with st.container():
            st.markdown("""
                <div style='background: linear-gradient(to right, #e3f2fd, #fff); padding: 2rem; border-radius: 10px;'>
                    <h3 style='color: #0d47a1; font-weight: 800; font-size: 2.2rem; margin-bottom: 0.2rem;'>👤 Mi Perfil</h3>
                    <p style='font-size:1.3rem; color: #333;'>Revisa la información personal del usuario activo.</p>
                </div>
            """, unsafe_allow_html=True)
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
            st.markdown("""
                <div style='background: linear-gradient(to right, #e3f2fd, #fff); padding: 2rem; border-radius: 10px;'>
                    <h3 style='color: #0d47a1; font-weight: 800; font-size: 2.2rem; margin-bottom: 0.2rem;'>📦 Gestión de Pedidos</h3>
                    <p style='font-size:1.3rem; color: #333;'>Crea, visualiza y administra pedidos de uniformes.</p>
                </div>
            """, unsafe_allow_html=True)
            with Session(engine) as session:
                if role in ["ventas", "admin"]:
                    st.subheader("Crear nuevo pedido")
                    with st.form("crear_pedido"):
                        cliente = st.text_input("Nombre del Cliente")
                        direccion = st.text_input("Dirección del Cliente")
                        es_muestra = st.radio("¿Es muestra o pedido?", ["Muestra", "Pedido"])
                        prenda = st.selectbox("Tipo de prenda", ["Camisa", "Pantalón", "Chamarra", "Chaleco"])
                        tela = st.selectbox("Tipo de tela", ["Mezclilla", "Kakhi", "Poliéster"])
                        color = st.text_input("Color de la tela")
                        talla = st.text_input("Talla")
                        cantidad = st.number_input("Cantidad de prendas", min_value=1, value=1)
                        fecha_entrega = st.date_input("Fecha estimada de entrega")

                        st.markdown("### Materiales")
                        boton = st.selectbox("Tipo de botón", ["Plástico", "Metal", "Nácar"])
                        cierre = st.selectbox("Tipo de cierre", ["Nylon", "Metálico", "Velcro"])
                        estampado = st.selectbox("Estampado", ["Ninguno", "Serigrafía", "Sublimado"])
                        bordado = st.selectbox("Bordado", ["Ninguno", "Logo empresa", "Nombre empleado"])

                        submitted = st.form_submit_button("Crear pedido")

                        if submitted:
                            precio_unitario = {"Camisa": 100, "Pantalón": 200, "Chamarra": 300, "Chaleco": 150}[prenda]
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
                            st.success("Pedido creado correctamente.")
                    st.markdown("---")

                st.subheader("Lista de pedidos")
                if role == "admin":
                    pedidos = session.exec(select(Pedido)).all()
                else:
                    pedidos = session.exec(select(Pedido).where(Pedido.usuario_id == st.session_state.user.id)).all()

                for p in pedidos:
                    with st.expander(f"📦 Pedido #{p.id} — Cliente: {p.cliente} — Fecha: {p.fecha.strftime('%Y-%m-%d')} — Estado: {p.status.capitalize()}"):
                        st.markdown(f"**Dirección del Cliente:** {p.direccion if hasattr(p, 'direccion') else 'N/D'}")
                        st.markdown(f"**Tipo de Pedido:** {'Muestra' if getattr(p, 'es_muestra', False) else 'Pedido'}")
                        st.markdown(f"**Prenda:** {getattr(p, 'prenda', 'N/D')} — **Tela:** {getattr(p, 'tela', 'N/D')} — **Color:** {getattr(p, 'color', 'N/D')}")
                        st.markdown(f"**Talla:** {getattr(p, 'talla', 'N/D')} — **Cantidad:** {getattr(p, 'cantidad', 'N/D')}")
                        st.markdown(f"**Fecha Estimada de Entrega:** {getattr(p, 'fecha_entrega', 'N/D')}")
                        st.markdown("**Materiales:**")
                        st.markdown(f"- Botón: {getattr(p, 'boton', 'N/D')}")
                        st.markdown(f"- Cierre: {getattr(p, 'cierre', 'N/D')}")
                        st.markdown(f"- Estampado: {getattr(p, 'estampado', 'N/D')}")
                        st.markdown(f"- Bordado: {getattr(p, 'bordado', 'N/D')}")

                        precio_unitario = {"Camisa": 100, "Pantalón": 200, "Chamarra": 300, "Chaleco": 150}.get(getattr(p, "prenda", ""), 0)
                        cantidad = getattr(p, "cantidad", 1)
                        st.markdown(f"**Costo estimado:** ${precio_unitario * cantidad} MXN")

                        if role == "admin":
                            cols = st.columns(2)
                            with cols[0]:
                                if st.button(f"✅ Aprobar #{p.id}", key=f"aprobar_{p.id}"):
                                    p.status = "aprobado"
                                    session.add(p)
                                    session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido aprobado", timestamp=datetime.utcnow()))
                                    session.commit()
                                    st.rerun()
                            with cols[1]:
                                if st.button(f"❌ Rechazar #{p.id}", key=f"rechazar_{p.id}"):
                                    p.status = "rechazado"
                                    session.add(p)
                                    session.add(Bitacora(pedido_id=p.id, usuario_id=st.session_state.user.id, accion="Pedido rechazado", timestamp=datetime.utcnow()))
                                    session.commit()
                                    st.rerun()
        st.markdown("---")

    elif selected == "📝 Bitácora":
        with st.container():
            st.markdown("""
                <div style='background: linear-gradient(to right, #e3f2fd, #fff); padding: 2rem; border-radius: 10px;'>
                    <h3 style='color: #0d47a1; font-weight: 800; font-size: 2.2rem; margin-bottom: 0.2rem;'>📝 Historial de Acciones</h3>
                    <p style='font-size:1.3rem; color: #333;'>Consulta las acciones recientes relacionadas con pedidos.</p>
                </div>
            """, unsafe_allow_html=True)
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
            st.markdown("""
                <div style='background: linear-gradient(to right, #e3f2fd, #fff); padding: 2rem; border-radius: 10px;'>
                    <h3 style='color: #0d47a1; font-weight: 800; font-size: 2.2rem; margin-bottom: 0.2rem;'>📊 Dashboard de Reportes</h3>
                    <p style='font-size:1.3rem; color: #333;'>Análisis visual de pedidos por estado, usuario y fecha.</p>
                </div>
            """, unsafe_allow_html=True)
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
