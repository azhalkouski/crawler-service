from unittest.mock import MagicMock

import pytest
from crawler_service.context_managers.postgres_connection import PostgresConnection

db_name = "test_db"
user_name = "test_user"
user_pass = "test_pass"


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
