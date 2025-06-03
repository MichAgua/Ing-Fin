import streamlit as st

# Simulamos una "base de datos" de usuarios
USUARIOS = {
    "12345": {"password": "abc123", "rol": "ventas"},
    "56789": {"password": "trazo123", "rol": "trazo"},
    "admin": {"password": "admin123", "rol": "maestro"}
}

st.set_page_config(page_title="Sistema de Uniformes")

# Título
st.title("Sistema de Gestión de Pedidos de Uniformes")

# Sidebar con login
st.sidebar.title("Inicio de sesión")

usuario = st.sidebar.text_input("Usuario (número de empleado)")
password = st.sidebar.text_input("Contraseña", type="password")

# Botón para iniciar sesión
if st.sidebar.button("Iniciar sesión"):
    if usuario in USUARIOS and USUARIOS[usuario]["password"] == password:
        st.success(f"Bienvenido, usuario {usuario} ({USUARIOS[usuario]['rol']})")

        rol = USUARIOS[usuario]["rol"]

        # Muestra pantallas distintas según el rol
        if rol == "ventas":
            st.subheader("Panel de Ventas")
            st.write("Aquí podrás ver y aprobar pedidos.")
        elif rol == "trazo":
            st.subheader("Panel de Trazo")
            st.write("Aquí verás especificaciones para producción.")
        elif rol == "maestro":
            st.subheader("Panel Maestro")
            st.write("Acceso completo a todos los módulos.")
        else:
            st.warning("Rol no reconocido.")
    else:
        st.error("Usuario o contraseña incorrectos.")