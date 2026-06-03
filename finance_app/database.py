"""Configuração do banco SQLite e criação de tabelas."""

from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path


DATABASE_NAME = "finance_app.db"
APP_NAME = "Finkado"


def _get_user_data_dir() -> Path:
    """Retorna uma pasta gravável para dados quando o app está empacotado."""
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")) / APP_NAME
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / APP_NAME
    return Path(os.environ.get("XDG_DATA_HOME", Path.home() / ".local" / "share")) / APP_NAME


def _get_default_database_path() -> Path:
    """Usa pasta local no desenvolvimento e AppData quando executável."""
    if getattr(sys, "frozen", False):
        return _get_user_data_dir() / DATABASE_NAME
    return Path(__file__).resolve().parent / DATABASE_NAME


DATABASE_PATH = _get_default_database_path()


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
