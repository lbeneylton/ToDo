# Importação da Base
from todo.core.base import Base

# Classes e metodos do ORM para modelagem
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func  # Tipos do SqlAlchemy

from datetime import datetime

# Classe para modelo de task no banco de dados


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Dados da task criados pelo usuario
    titulo: Mapped[str] = mapped_column(String(30), nullable=False)
    descricao: Mapped[str] = mapped_column(String(300), default="")

    # Dados da task criados pelo sistema
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    data_atualizacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )

    # Estado da task (Pendente, Concluida)
    status: Mapped[str] = mapped_column(
        String(20),
        default="pendente",
        nullable=False
    )
