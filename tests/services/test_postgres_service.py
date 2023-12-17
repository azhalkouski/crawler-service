from unittest.mock import MagicMock, patch

import pytest
from crawler_service.services.abstract_db_service import AbstractDBService
from crawler_service.services.postgres_service import PostgresService

test_config = {
    "db_name": "test_db_name",
    "username": "test_username",
    "password": "test_password",
}


@pytest.fixture
def mock_open_service_config(monkeypatch):
    def mock_service_config():
        return test_config

    monkeypatch.setattr(
        "crawler_service.services.postgres_service.open_service_config",
        mock_service_config,
    )


@pytest.fixture
def mock_postgres_connection():
    with patch(
        "crawler_service.services.postgres_service.PostgresConnection"
    ) as mock_postgres_connection:
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_postgres_connection.return_value.__enter__.return_value = (
            mock_connection,
            mock_cursor,
        )
        yield mock_postgres_connection


def test_postgres_service_is_instance_of_abstract_db_service():
    assert issubclass(PostgresService, AbstractDBService)


def test_postgres_service_is_init_with_attrs_form_service_config(
    mock_open_service_config
):
    postgres_service = PostgresService()

    assert hasattr(postgres_service, "db_name")
    assert hasattr(postgres_service, "user_name")
    assert hasattr(postgres_service, "user_pass")

    assert postgres_service.db_name == test_config["db_name"]
    assert postgres_service.user_name == test_config["username"]
    assert postgres_service.user_pass == test_config["password"]


def test_load_all_cities(mock_open_service_config, mock_postgres_connection):
    cities_in_dv = [(1, "city_1"), (2, "city_2")]
    postgres_service = PostgresService()

    # Mock the execute method of the cursor
    mock_cursor = mock_postgres_connection.return_value.__enter__.return_value[1]
    mock_cursor.fetchall.return_value = cities_in_dv

    cities = postgres_service.load_all_cities()

    # Assert that the execute method was called with the correct sql
    mock_cursor.execute.assert_called_once_with("SELECT * FROM cities;")

    assert cities == cities_in_dv


def test_save_units_count(mock_open_service_config, mock_postgres_connection):
    city_id_arg = 1
    unit_type_arg = "apartment_unit_type"
    transaction_type_arg = "rent_transaction_type"
    count_arg = 10

    postgres_service = PostgresService()
    postgres_service.save_units_count(
        city_id_arg, unit_type_arg, transaction_type_arg, count_arg
    )

    # Assert that the execute method was called with the correct sql
    mock_cursor = mock_postgres_connection.return_value.__enter__.return_value[1]
    mock_cursor.execute.assert_called_once_with(
        f"""INSERT INTO total_counts_per_city\
                      (city_id, unit_type, transaction_type, total_count) VALUES\
                        ({city_id_arg}, '{unit_type_arg}', '{transaction_type_arg}',\
                          {count_arg});"""
    )

    # Assert that the commit method was called
    mock_connection = mock_postgres_connection.return_value.__enter__.return_value[0]
    mock_connection.commit.assert_called_once()
