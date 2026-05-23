from sqlalchemy.orm import Session  # Class Session
from sqlalchemy.exc import SQLAlchemyError  # Exceção do SQLAlchemy

# Classe task e objeto logger
from todo.models import Task
from todo.core.logger import logger as lg

from datetime import datetime


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # CREATE
    def create(self, task: Task) -> Task:
        try:
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            lg.info(f"Tarefa {task.id} Criada", task_id=task.id)
            return task

        except SQLAlchemyError as e:
            self.session.rollback()

            lg.error(
                f"Falha na criação da tarefa {task.id}",
                error=str(e),
                task_data=str(task),
                exc_info=True
            )
            raise

    # READ
    def get_by_id(self, task_id: int) -> Task | None:

        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            lg.info(
                f"Tarefa {task_id} encontrada",
                task_id=task_id
            )
            return task

        lg.error(
            f"Falha na busca da tarefa por id {task_id}",
            task_id=str(task_id)
        )
        return None

    def get_by_status(self, status: str):
        return self.session.query(Task).filter(Task.status == status).all()

    # UPDATE
    def update(self, task: Task) -> Task:
        """
        Atualiza a tarefa no banco.
        """
        try:
            # Atualiza a data de atualização automaticamente
            task.data_atualizacao = datetime.now()
            # Como o objeto já está vinculado à sessão, commit salva as alterações
            self.session.commit()
            # garante que o objeto Python está sincronizado com o DB
            self.session.refresh(task)
            lg.info(
                f"Tarefa {task.id} atualizada",
                task_id=task.id
            )
            return task

        except SQLAlchemyError as e:
            lg.error(
                f"Falha ao atualizar a tarefa {task.id}",
                error=str(e),
                task_id=str(task.id),
                exc_info=True
            )
            raise

    # DELETE
    def delete(self, task: Task):
        self.session.delete(task)
        self.session.commit()
