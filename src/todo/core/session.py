"""Script para obter sessão do banco
para execuçaõ de querys com auto fechamento de sessão
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

URL_BASE = ""

engine = create_engine(URL_BASE)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
