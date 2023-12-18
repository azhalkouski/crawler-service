from unittest.mock import MagicMock

import psycopg2
import pytest
from crawler_service.context_managers.postgres_connection import PostgresConnection

db_name = "test_db"
user_name = "test_user"
user_pass = "test_pass"

exceprion_e = {
    "exc_type": Exception,
    "exc_value": "Test exception",
    "traceback": MagicMock(),
}


@pytest.fixture
def mock_psycopg2_connect(monkeypatch):
    connection_magic_mock = MagicMock()
    cursor_magic_mock = MagicMock()

    def mock_connect(*args, **kwargs):
        connection = connection_magic_mock
        cursor = cursor_magic_mock
        connection.cursor.return_value = cursor
        return connection

    magic_mock_connect = MagicMock(side_effect=mock_connect)
    monkeypatch.setattr(
        "crawler_service.context_managers.postgres_connection.psycopg2.connect",
        magic_mock_connect,
    )

    return connection_magic_mock, cursor_magic_mock, magic_mock_connect


def test_postgres_connection_inited_with_passed_params():
    """Test that PostgresConnection is inited with passed params"""

    postgres_connection = PostgresConnection(db_name, user_name, user_pass)

    assert postgres_connection.db_name == db_name
    assert postgres_connection.user_name == user_name
    assert postgres_connection.user_pass == user_pass


def test_postgres_connection_connects_to_psycopg2_with_passed_params(
    mock_psycopg2_connect
):
    """Test that PostgresConnection connects to psycopg2 with passed params"""

    _, _, magic_mock_connect = mock_psycopg2_connect

    with PostgresConnection(db_name, user_name, user_pass) as (conn, cur):
        magic_mock_connect.assert_called_once_with(
            f"dbname={db_name} user={user_name} password={user_pass}"
        )


def test_postgres_connection__enter__returns_connection_and_cursor(
    mock_psycopg2_connect
):
    """Test that __enter__ method returns connection and cursor"""

    connection_mock, cursor_mock, magic_mock_connect = mock_psycopg2_connect

    with PostgresConnection(db_name, user_name, user_pass) as (conn, cur):
        assert conn == connection_mock
        assert cur == cursor_mock


def test_postgres_connection_handles_operational_error(mock_psycopg2_connect):
    """Test that PostgresConnection handles psycopg2 OperationalError"""

    _, _, magic_mock_connect = mock_psycopg2_connect
    operational_error = "Operational error"
    magic_mock_connect.side_effect = psycopg2.OperationalError(operational_error)

    postgres_connection = PostgresConnection(db_name, user_name, user_pass)
    error_logger_mock = MagicMock()
    postgres_connection.error_logger.error = error_logger_mock

    postgres_connection.__enter__()

    error_logger_mock.assert_called_once_with(
        f"psycopg2::operational error: {operational_error}"
    )


def test_postgres_connection_handles_programming_error(mock_psycopg2_connect):
    """Test that PostgresConnection handles psycopg2 ProgrammingError"""

    _, _, magic_mock_connect = mock_psycopg2_connect
    operational_error = "Programming error"
    magic_mock_connect.side_effect = psycopg2.ProgrammingError(operational_error)

    postgres_connection = PostgresConnection(db_name, user_name, user_pass)
    postgres_connection.__enter__()


def test_postgres_connection_handles_generic_exception(mock_psycopg2_connect):
    """Test that PostgresConnection handles generic exceptions"""

    _, _, magic_mock_connect = mock_psycopg2_connect
    exception_message = "Something happened at db interaction level"
    magic_mock_connect.side_effect = Exception(exception_message)

    postgres_connection = PostgresConnection(db_name, user_name, user_pass)
    critical_logger_mock = MagicMock()
    postgres_connection.critical_logger.critical = critical_logger_mock

    postgres_connection.__enter__()

    critical_logger_mock.assert_called_once_with(
        f"Something happened at db interaction level: {exception_message}"
    )


def test_postgres_connection__exit__closes_connection_when_no_exception():
    """Test that __exit__ method closes the connection when there is no exception"""

    postgres_connection = PostgresConnection(db_name, user_name, user_pass)
    cursor_mock = MagicMock()
    conn_mock = MagicMock()
    postgres_connection.cursor = cursor_mock
    postgres_connection.conn = conn_mock

    postgres_connection.__exit__(None, None, None)

    cursor_mock.close.assert_called_once()
    conn_mock.close.assert_called_once()


def test_postgres_connection_exit_closes_connection_when_exception_occurs():
    """Test that __exit__ method closes the connection when there is an exception"""

    postgres_connection = PostgresConnection(db_name, user_name, user_pass)
    cursor_mock = MagicMock()
    conn_mock = MagicMock()
    postgres_connection.cursor = cursor_mock
    postgres_connection.conn = conn_mock

    postgres_connection.__exit__(
        exceprion_e["exc_type"], exceprion_e["exc_value"], exceprion_e["traceback"]
    )

    cursor_mock.close.assert_called_once()
    conn_mock.close.assert_called_once()


def test_postgres_connection_exit_logs_exception_when_exception_occurs():
    """Test that __exit__ method logs the exception when there is an exception"""

    postgres_connection = PostgresConnection(db_name, user_name, user_pass)
    cursor_mock = MagicMock()
    conn_mock = MagicMock()
    postgres_connection.cursor = cursor_mock
    postgres_connection.conn = conn_mock
    error_logger_mock = MagicMock()
    postgres_connection.error_logger.error = error_logger_mock

    exc_type, exc_value, traceback = exceprion_e.values()

    postgres_connection.__exit__(exc_type, exc_value, traceback)

    error_logger_mock.assert_called_once_with(f"{exc_type} | {exc_value} | {traceback}")
