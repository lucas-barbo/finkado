# Gestor Financeiro Pessoal

Aplicação desktop básica para controle financeiro pessoal, desenvolvida em Python com interface gráfica em Tkinter e persistência local em SQLite.

O sistema permite cadastrar receitas e despesas, visualizar um dashboard financeiro simples e acompanhar todas as transações em uma tabela interativa.

## Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![Arquitetura](https://img.shields.io/badge/Architecture-Modular-orange)

- **Python 3.10+**
- **Tkinter** para interface gráfica desktop
- **SQLite** com a biblioteca nativa `sqlite3`
- **Arquitetura em camadas** separando interface, regras de negócio e acesso a dados

## Arquitetura do Projeto

```text
finance_app/
│
├── main.py
├── database.py
│
├── models/
│   └── transaction.py
│
├── repositories/
│   └── transaction_repo.py
│
└── views/
    └── main_window.py
```

### Organização das Camadas

- **`main.py`**: ponto de entrada da aplicação. Inicializa o banco de dados, cria o repositório e abre a janela principal.
- **`database.py`**: centraliza a conexão com o SQLite e a criação automática das tabelas necessárias.
- **`models/`**: contém as entidades do domínio, como a classe `Transaction`, que representa uma transação financeira.
- **`repositories/`**: concentra as operações de acesso a dados, como criação, listagem, exclusão e cálculo de resumo financeiro.
- **`views/`**: contém a interface gráfica, mantendo a camada visual separada das regras de negócio e das queries SQL.

Essa divisão facilita manutenção, testes futuros e evolução do projeto, evitando que interface, persistência e lógica fiquem misturadas no mesmo arquivo.

## Pré-requisitos

Antes de executar o projeto, certifique-se de ter instalado:

- **Python 3.10 ou superior**
- **Tkinter disponível no ambiente Python**

Na maioria das instalações do Python, o Tkinter já vem incluído. Em algumas distribuições Linux, pode ser necessário instalar o pacote do sistema:

```bash
sudo apt install python3-tk
```

## Instalação e Execução

### 1. Obter o projeto

Clone o repositório ou crie a estrutura de pastas do projeto localmente:

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

Caso esteja criando manualmente, mantenha a estrutura:

```text
finance_app/
requirements.txt
README.md
```

### 2. Criar um ambiente virtual

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar as dependências

O projeto usa apenas bibliotecas nativas do Python. Mesmo assim, você pode executar o comando abaixo para manter o fluxo padrão de instalação:

```bash
pip install -r requirements.txt
```

### 4. Executar a aplicação

A partir da raiz do projeto, execute:

```bash
python -m finance_app.main
```

Também é possível entrar na pasta da aplicação e rodar diretamente o arquivo principal:

```bash
cd finance_app
python main.py
```

## Funcionalidades Principais

- Visualizar um dashboard com **Saldo Total**, **Total de Receitas** e **Total de Despesas**.
- Listar todas as transações cadastradas em uma tabela.
- Cadastrar novas transações com descrição, valor, tipo, categoria e data.
- Validar campos obrigatórios no cadastro.
- Validar se o valor informado é numérico e maior que zero.
- Excluir uma transação selecionada na tabela.
- Atualizar automaticamente os totais financeiros após cadastro ou exclusão.

## Persistência de Dados

O banco de dados SQLite é criado automaticamente na primeira execução da aplicação, caso ainda não exista.

Por padrão, o arquivo local é gerado em:

```text
finance_app/finance_app.db
```

Esse arquivo armazena as transações cadastradas e permite que os dados continuem disponíveis nas próximas execuções do app.

