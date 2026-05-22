from unittest.mock import MagicMock, patch

from ..src.todo.core.session import get_session


def test_get_session_fecha_sessao():
    # Mock da sessão
    mock_session = MagicMock()

    # Mock do SessionLocal retornando a sessão fake
    with patch("seu_modulo.SessionLocal", return_value=mock_session):

        # Executa o generator
        generator = get_session()

        # Obtém a sessão do yield
        session = next(generator)

        # Verifica se retornou corretamente
        assert session == mock_session

        # Finaliza generator para executar finally
        try:
            next(generator)
        except StopIteration:
            pass

        # Verifica se close foi chamado
        mock_session.close.assert_called_once()
