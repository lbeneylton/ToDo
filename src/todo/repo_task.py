from sqlalchemy.orm import Session  # Class Session
from sqlalchemy.exc import SQLAlchemyError  # Exceção do SQLAlchemy

# Classe task e objeto logger
from model_task import Task
from core.logger import logger as lg


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    # CREATE
    def create(self, task: Task) -> Task:
        try:
            self.session.add(task)
            self.session.commit()
            self.session.refresh(task)

            lg.info("Tarefa Criada", task_id=task.id)
            return task

        except SQLAlchemyError as e:
            self.session.rollback()

            lg.error(
                "Falha na criação da tarefa",
                error=str(e),
                task_data=str(task),
                exc_info=True
            )
            raise

    # READ
    def get_by_id(self, task_id: int) -> Task | None:
        return self.session.query(Task).filter(Task.id == task_id).first()

    def get_by_status(self, status: str):
        return self.session.query(Task).filter(Task.status == status).all()

    # UPDATE
    def update(self):
        self.session.commit()

    # DELETE
    def delete(self, task: Task):
        self.session.delete(task)
        self.session.commit()
