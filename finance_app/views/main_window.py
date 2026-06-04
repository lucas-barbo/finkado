"""Janela principal da aplicação financeira."""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk

from finance_app.models.transaction import Transaction, VALID_TRANSACTION_TYPES
from finance_app.repositories.transaction_repo import TransactionRepository


class MainWindow:
    """Interface gráfica principal com dashboard, tabela e formulário."""

    def __init__(self, root: tk.Tk, repository: TransactionRepository) -> None:
        self.root = root
        self.repository = repository
        self.balance_var = tk.StringVar(value="R$ 0,00")
        self.income_var = tk.StringVar(value="R$ 0,00")
        self.expenses_var = tk.StringVar(value="R$ 0,00")

        self._configure_window()
        self._configure_styles()
        self._build_layout()
        self.refresh_data()

    def run(self) -> None:
        """Inicia o loop da interface."""
        self.root.mainloop()

    def _configure_window(self) -> None:
        self.root.title("Gestor Financeiro Pessoal")
        self.root.geometry("980x620")
        self.root.minsize(860, 540)
        self.root.configure(bg="#f4f6f8")

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TFrame", background="#f4f6f8")
        style.configure("Card.TFrame", background="#ffffff", relief="flat")
        style.configure("TLabel", background="#f4f6f8", foreground="#263238", font=("Arial", 10))
        style.configure("Title.TLabel", font=("Arial", 18, "bold"))
        style.configure("CardTitle.TLabel", background="#ffffff", foreground="#607d8b", font=("Arial", 10, "bold"))
        style.configure("CardValue.TLabel", background="#ffffff", foreground="#263238", font=("Arial", 16, "bold"))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=8)
        style.configure(
            "Treeview",
            background="#ffffff",
            fieldbackground="#ffffff",
            foreground="#263238",
            rowheight=28,
            font=("Arial", 10),
        )
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), padding=8)

    def _build_layout(self) -> None:
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(main_frame)
        header.pack(fill=tk.X, pady=(0, 16))

        ttk.Label(header, text="Gestor Financeiro Pessoal", style="Title.TLabel").pack(side=tk.LEFT)

        button_frame = ttk.Frame(header)
        button_frame.pack(side=tk.RIGHT)
        ttk.Button(button_frame, text="Nova Transação", command=self.open_transaction_form).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(button_frame, text="Excluir Selecionada", command=self.delete_selected_transaction).pack(side=tk.LEFT)

        dashboard = ttk.Frame(main_frame)
        dashboard.pack(fill=tk.X, pady=(0, 18))
        dashboard.columnconfigure((0, 1, 2), weight=1, uniform="dashboard")

        self._create_dashboard_card(dashboard, 0, "Saldo Total", self.balance_var)
        self._create_dashboard_card(dashboard, 1, "Total de Receitas", self.income_var)
        self._create_dashboard_card(dashboard, 2, "Total de Despesas", self.expenses_var)

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("id", "description", "amount", "type", "category", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", selectmode="browse")

        self.tree.heading("id", text="ID")
        self.tree.heading("description", text="Descrição")
        self.tree.heading("amount", text="Valor")
        self.tree.heading("type", text="Tipo")
        self.tree.heading("category", text="Categoria")
        self.tree.heading("date", text="Data")

        self.tree.column("id", width=60, anchor=tk.CENTER, stretch=False)
        self.tree.column("description", width=280, anchor=tk.W)
        self.tree.column("amount", width=120, anchor=tk.E, stretch=False)
        self.tree.column("type", width=110, anchor=tk.CENTER, stretch=False)
        self.tree.column("category", width=160, anchor=tk.W)
        self.tree.column("date", width=110, anchor=tk.CENTER, stretch=False)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def _create_dashboard_card(self, parent: ttk.Frame, column: int, title: str, variable: tk.StringVar) -> None:
        card = ttk.Frame(parent, style="Card.TFrame", padding=16)
        card.grid(row=0, column=column, sticky="ew", padx=6)
        ttk.Label(card, text=title, style="CardTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(card, textvariable=variable, style="CardValue.TLabel").pack(anchor=tk.W, pady=(8, 0))

    def refresh_data(self) -> None:
        """Atualiza dashboard e tabela após qualquer alteração."""
        try:
            summary = self.repository.get_summary()
            transactions = self.repository.list_all()
        except RuntimeError as error:
            messagebox.showerror("Erro", str(error))
            return

        self.balance_var.set(self._format_currency(summary["balance"]))
        self.income_var.set(self._format_currency(summary["income"]))
        self.expenses_var.set(self._format_currency(summary["expenses"]))

        self.tree.delete(*self.tree.get_children())
        for transaction in transactions:
            self.tree.insert(
                "",
                tk.END,
                iid=str(transaction.id),
                values=(
                    transaction.id,
                    transaction.description,
                    self._format_currency(transaction.amount),
                    transaction.type,
                    transaction.category,
                    transaction.date,
                ),
            )

    def open_transaction_form(self) -> None:
        """Abre uma janela modal para cadastrar transações."""
        form = tk.Toplevel(self.root)
        form.title("Nova Transação")
        form.geometry("420x340")
        form.resizable(False, False)
        form.configure(bg="#f4f6f8")
        form.transient(self.root)
        form.grab_set()

        container = ttk.Frame(form, padding=20)
        container.pack(fill=tk.BOTH, expand=True)

        description_var = tk.StringVar()
        amount_var = tk.StringVar()
        type_var = tk.StringVar(value=VALID_TRANSACTION_TYPES[0])
        category_var = tk.StringVar()
        date_var = tk.StringVar(value=Transaction.today_iso())

        self._create_form_field(container, "Descrição", description_var, 0)
        self._create_form_field(container, "Valor", amount_var, 1)

        ttk.Label(container, text="Tipo").grid(row=2, column=0, sticky=tk.W, pady=(0, 6))
        type_combo = ttk.Combobox(container, textvariable=type_var, values=VALID_TRANSACTION_TYPES, state="readonly")
        type_combo.grid(row=2, column=1, sticky="ew", pady=(0, 12))

        self._create_form_field(container, "Categoria", category_var, 3)
        self._create_form_field(container, "Data", date_var, 4)

        container.columnconfigure(1, weight=1)

        actions = ttk.Frame(container)
        actions.grid(row=5, column=0, columnspan=2, sticky=tk.E, pady=(14, 0))
        ttk.Button(actions, text="Cancelar", command=form.destroy).pack(side=tk.RIGHT)
        ttk.Button(
            actions,
            text="Salvar",
            command=lambda: self._save_transaction(
                form,
                description_var.get(),
                amount_var.get(),
                type_var.get(),
                category_var.get(),
                date_var.get(),
            ),
        ).pack(side=tk.RIGHT, padx=(0, 8))

        form.bind("<Return>", lambda _event: self._save_transaction(
            form,
            description_var.get(),
            amount_var.get(),
            type_var.get(),
            category_var.get(),
            date_var.get(),
        ))
        form.bind("<Escape>", lambda _event: form.destroy())

    def _create_form_field(self, parent: ttk.Frame, label: str, variable: tk.StringVar, row: int) -> None:
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky=tk.W, pady=(0, 6))
        entry = ttk.Entry(parent, textvariable=variable)
        entry.grid(row=row, column=1, sticky="ew", pady=(0, 12))

    def _save_transaction(
        self,
        form: tk.Toplevel,
        description: str,
        amount_text: str,
        transaction_type: str,
        category: str,
        transaction_date: str,
    ) -> None:
        try:
            amount = self._parse_amount(amount_text)
            transaction = Transaction(
                description=description,
                amount=amount,
                type=transaction_type,
                category=category,
                date=transaction_date,
            )
            self.repository.create(transaction)
        except ValueError as error:
            messagebox.showwarning("Dados inválidos", str(error), parent=form)
            return
        except RuntimeError as error:
            messagebox.showerror("Erro", str(error), parent=form)
            return

        form.destroy()
        self.refresh_data()

    def delete_selected_transaction(self) -> None:
        """Exclui a transação selecionada na tabela."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showinfo("Seleção necessária", "Selecione uma transação para excluir.")
            return

        transaction_id = int(selected_item[0])
        confirm = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir a transação #{transaction_id}?",
        )
        if not confirm:
            return

        try:
            self.repository.delete(transaction_id)
        except (RuntimeError, ValueError) as error:
            messagebox.showerror("Erro", str(error))
            return

        self.refresh_data()

    @staticmethod
    def _parse_amount(amount_text: str) -> float:
        normalized_amount = amount_text.strip().replace("R$", "").strip()
        if not normalized_amount:
            raise ValueError("O valor é obrigatório.")

        if "," in normalized_amount and "." in normalized_amount:
            if normalized_amount.rfind(",") > normalized_amount.rfind("."):
                normalized_amount = normalized_amount.replace(".", "").replace(",", ".")
            else:
                normalized_amount = normalized_amount.replace(",", "")
        elif "," in normalized_amount:
            normalized_amount = normalized_amount.replace(",", ".")

        try:
            amount = float(normalized_amount)
        except ValueError as error:
            raise ValueError("O valor deve ser numérico.") from error

        if amount <= 0:
            raise ValueError("O valor deve ser maior que zero.")
        return amount

    @staticmethod
    def _format_currency(value: float) -> str:
        formatted = f"{value:,.2f}"
        formatted = formatted.replace(",", "X").replace(".", ",").replace("X", ".")
        return f"R$ {formatted}"
