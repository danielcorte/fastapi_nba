from sqlalchemy import Column, Integer, String, Float, create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from typing import List, Optional

# Configuração do banco de dados SQLite
DATABASE_URL = "sqlite:///./nba.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Modelo SQLAlchemy (Banco de Dados)
class TeamDB(Base):
    __tablename__ = "teams"
    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    city = Column(String)
    championships = Column(Integer)
    founded = Column(Integer)
    market_value = Column(Float)
    conference_titles = Column(Integer)
    conference = Column(String)

# Criando a tabela no banco
Base.metadata.create_all(bind=engine)

# Dependência para obter sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()