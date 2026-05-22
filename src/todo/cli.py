import typer
from todo.repo.task import TaskRepository
from todo.models.model_task import Task
from core.session import get_session

cli = typer.Typer()


@cli.command()
def add(titulo: str, descricao: str = ""):

    session = next(get_session())
    repo = TaskRepository(session)

    task = Task(titulo=titulo, descricao=descricao)
    repo.create(task)

    typer.echo(f"Tarefa criada com ID {task.id}")


if __name__ == "__main__":
    cli()
