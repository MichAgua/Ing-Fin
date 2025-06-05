from sqlmodel import SQLModel, create_engine

# Reemplaza esto con tu ruta real de base de datos
DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL, echo=True)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session