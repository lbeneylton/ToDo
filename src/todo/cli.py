import typer
from repo_task import TaskRepository

cli = typer.Typer()


@cli.command()
def add(titulo: str, descricao: str = ""):
    pass


if __name__ == "__main__":
    cli()
