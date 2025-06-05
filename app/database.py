from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///uniformes.db"
engine = create_engine(DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

with Session(engine) as session:
    try:
        st.write("🔍 Consultando pedidos...")
        pedidos = session.exec(select(Pedido)).all()
        st.success("Pedidos cargados correctamente.")
    except Exception as e:
        st.error(f"⚠️ Error al cargar pedidos: {e}")