import typer
from datetime import datetime
from todo.service.task import TaskService

cli = typer.Typer(help="Aplicativo de gerenciamento de tarefas.")

service = TaskService()  # inicializa uma vez


def format_datetime(dt):
    if isinstance(dt, str):
        dt = datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
    return dt.strftime("%d/%m/%Y %H:%M")


@cli.command()
def add(
    titulo: str,
    descricao: str = typer.Option(
        "", "--descricao", "-d", help="Descrição da tarefa")
):
    """Adiciona uma tarefa com titulo obrigatorio e descrição opcional, o status inicial é pendente"""
    task = service.criar(titulo, descricao)
    typer.echo(f"Tarefa criada com ID {task.id}")


@cli.command()
def listar(
    quantidade: int = 10,
    status: str = typer.Option(
        "pendente", "--status", "-s", help="Status da tarefa [concluida, pendente]")
):
    """Retorna uma quantidade específica de tarefas com base em seu status, por padrão mostra as 10 ultimas pendentes"""

    tasks = service.listar(status)

    for task in tasks:
        typer.echo(f"Título             : {task.titulo}")
        typer.echo(
            f"Data Criação       : {format_datetime(task.data_criacao)}")
        typer.echo(
            f"Última Atualização : {format_datetime(task.data_atualizacao)}")
        typer.echo(f"Status             : {task.status}")
        typer.echo("-" * 40)


@cli.command()
def marcar(id: int, status: str = "concluída"):
    """Atribui um status a uma tarefa, precisa do id da tarefa, o status padrão é concluída"""
    task = service.atualizar_status(id, status)
    if not task:
        typer.echo(f"Tarefa {id} não encontrada")
        raise typer.Exit(code=1)
    typer.echo(f"Tarefa {id} marcada como '{status}'")


if __name__ == "__main__":
    cli()


# editar → altera título/descrição
# deletar → remove tarefa
# resumo → mostra contagem de pendentes/concluídas
# limpar → remove todas concluídas
# exportar / importar → CSV
# Todas as funções com help para Typer
