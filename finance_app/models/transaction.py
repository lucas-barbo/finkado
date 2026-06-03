"""Entidade que representa uma transação financeira."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date as date_type


VALID_TRANSACTION_TYPES = ("Receita", "Despesa")


@dataclass(slots=True)
class Transaction:
    """Dados de uma receita ou despesa."""

    description: str
    amount: float
    type: str
    category: str
    date: str
    id: int | None = None

    def __post_init__(self) -> None:
        self.description = self.description.strip()
        self.category = self.category.strip()
        self.date = self.date.strip()

        if not self.description:
            raise ValueError("A descrição é obrigatória.")
        if not self.category:
            raise ValueError("A categoria é obrigatória.")
        if self.type not in VALID_TRANSACTION_TYPES:
            raise ValueError("O tipo deve ser 'Receita' ou 'Despesa'.")
        if self.amount <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        if not self.date:
            raise ValueError("A data é obrigatória.")

    @classmethod
    def from_row(cls, row: object) -> "Transaction":
        """Cria uma transação a partir de uma linha retornada pelo SQLite."""
        return cls(
            id=row["id"],
            description=row["description"],
            amount=float(row["amount"]),
            type=row["type"],
            category=row["category"],
            date=row["date"],
        )

    @staticmethod
    def today_iso() -> str:
        """Retorna a data atual no formato YYYY-MM-DD."""
        return date_type.today().isoformat()

