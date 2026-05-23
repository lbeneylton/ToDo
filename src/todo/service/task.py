import typer
from typing import List, Optional
from todo.repo.task import TaskRepository
from todo.core.session import get_session
from todo.models import Task


class TaskService:
    def __init__(self):
        # Inicializa a sessão e o repositório
        self.session = next(get_session())
        self.repo = TaskRepository(self.session)

    # CREATE
    def criar(self, titulo: str, descricao: str = "") -> Task:
        task = Task(titulo=titulo, descricao=descricao)
        return self.repo.create(task)

    # READ
    def listar(self, status: Optional[str] = None) -> List[Task]:
        if status:
            return self.repo.get_by_status(status)
        return self.repo.get_all()

    def buscar_por_id(self, task_id: int) -> Optional[Task]:
        return self.repo.get_by_id(task_id)

    # UPDATE
    def atualizar_status(self, task_id: int, status: str) -> Task | None:
        task = self.buscar_por_id(task_id)
        if not task:
            return None
        task.status = status
        return self.repo.update(task)

    def editar(self, task_id: int, titulo: str | None = None, descricao: str | None = None) -> Task:
        task = self.buscar_por_id(task_id)
        if not task:
            raise

        if titulo:
            task.titulo = titulo

        if descricao:
            task.descricao = descricao

        return self.repo.update(task)

    # DELETE
    def deletar(self, task_id: int):
        task = self.buscar_por_id(task_id)
        if task:
            self.repo.delete(task)

    # RESUMO
    def resumo(self):
        todas = self.repo.get_all()
        pendentes = [t for t in todas if t.status == "pendente"]
        concluidas = [t for t in todas if t.status == "concluída"]
        return {
            "total": len(todas),
            "pendentes": len(pendentes),
            "concluidas": len(concluidas)
        }
