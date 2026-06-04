"""CRUD de transações financeiras no SQLite."""

from __future__ import annotations

import sqlite3
from pathlib import Path

from finance_app.database import get_connection
from finance_app.models.transaction import Transaction


class TransactionRepository:
    """Encapsula todas as consultas SQL relacionadas a transações."""

    def __init__(self, db_path: Path | str) -> None:
        self.db_path = Path(db_path)

    def create(self, transaction: Transaction) -> int:
        """Insere uma transação e retorna o ID gerado."""
        sql = """
            INSERT INTO transactions (description, amount, type, category, date)
            VALUES (?, ?, ?, ?, ?);
        """
        params = (
            transaction.description,
            transaction.amount,
            transaction.type,
            transaction.category,
            transaction.date,
        )

        try:
            with get_connection(self.db_path) as connection:
                cursor = connection.execute(sql, params)
                connection.commit()
                return int(cursor.lastrowid)
        except sqlite3.Error as error:
            raise RuntimeError(f"Erro ao cadastrar transação: {error}") from error

    def list_all(self) -> list[Transaction]:
        """Lista todas as transações, das mais recentes para as mais antigas."""
        sql = """
            SELECT id, description, amount, type, category, date
            FROM transactions
            ORDER BY date DESC, id DESC;
        """

        try:
            with get_connection(self.db_path) as connection:
                rows = connection.execute(sql).fetchall()
                return [Transaction.from_row(row) for row in rows]
        except sqlite3.Error as error:
            raise RuntimeError(f"Erro ao listar transações: {error}") from error

    def delete(self, transaction_id: int) -> None:
        """Remove uma transação pelo ID."""
        sql = "DELETE FROM transactions WHERE id = ?;"

        try:
            with get_connection(self.db_path) as connection:
                cursor = connection.execute(sql, (transaction_id,))
                connection.commit()

                if cursor.rowcount == 0:
                    raise ValueError("Transação não encontrada.")
        except sqlite3.Error as error:
            raise RuntimeError(f"Erro ao excluir transação: {error}") from error

    def get_summary(self) -> dict[str, float]:
        """Calcula receitas, despesas e saldo total."""
        sql = """
            SELECT
                COALESCE(SUM(CASE WHEN type = 'Receita' THEN amount ELSE 0 END), 0) AS income,
                COALESCE(SUM(CASE WHEN type = 'Despesa' THEN amount ELSE 0 END), 0) AS expenses
            FROM transactions;
        """

        try:
            with get_connection(self.db_path) as connection:
                row = connection.execute(sql).fetchone()
                income = float(row["income"])
                expenses = float(row["expenses"])
                return {
                    "income": income,
                    "expenses": expenses,
                    "balance": income - expenses,
                }
        except sqlite3.Error as error:
            raise RuntimeError(f"Erro ao calcular resumo financeiro: {error}") from error
