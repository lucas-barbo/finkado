"""Configuração do banco SQLite e criação de tabelas."""

from __future__ import annotations

import sqlite3
from pathlib import Path


DATABASE_NAME = "finance_app.db"
DATABASE_PATH = Path(__file__).resolve().parent / DATABASE_NAME


def get_connection(db_path: Path | str = DATABASE_PATH) -> sqlite3.Connection:
    """Cria uma conexão SQLite com suporte a linhas nomeadas."""
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        return connection
    except sqlite3.Error as error:
        raise RuntimeError(f"Não foi possível conectar ao banco de dados: {error}") from error


def initialize_database(db_path: Path | str = DATABASE_PATH) -> Path:
    """Cria o arquivo .db e a tabela de transações, caso não existam."""
    database_path = Path(db_path)
    database_path.parent.mkdir(parents=True, exist_ok=True)

    create_table_sql = """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            amount REAL NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('Receita', 'Despesa')),
            category TEXT NOT NULL,
            date TEXT NOT NULL
        );
    """

    try:
        with get_connection(database_path) as connection:
            connection.execute(create_table_sql)
            connection.commit()
    except sqlite3.Error as error:
        raise RuntimeError(f"Não foi possível criar as tabelas: {error}") from error

    return database_path

