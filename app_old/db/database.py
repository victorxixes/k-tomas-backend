from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./k_tomas.db"  # Puedes cambiar a PostgreSQL más adelante

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# 🔥 ESTA FUNCIÓN ES OBLIGATORIA PARA FASTAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

