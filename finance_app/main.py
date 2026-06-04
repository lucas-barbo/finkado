"""Ponto de entrada da aplicação."""

from __future__ import annotations

import sys
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

if __package__ in {None, ""}:
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from finance_app.database import initialize_database
from finance_app.repositories.transaction_repo import TransactionRepository
from finance_app.views.main_window import MainWindow


def main() -> None:
    """Inicializa o banco, o repositório e a janela principal."""
    root = tk.Tk()
    root.withdraw()

    try:
        db_path = initialize_database()
        repository = TransactionRepository(db_path)
    except RuntimeError as error:
        messagebox.showerror("Erro ao iniciar", str(error))
        root.destroy()
        return

    root.deiconify()
    app = MainWindow(root, repository)
    app.run()


if __name__ == "__main__":
    main()
