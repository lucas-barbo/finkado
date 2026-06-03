# Gestor Financeiro Pessoal

Aplicação desktop básica para controle financeiro pessoal, desenvolvida em Python com interface gráfica em Tkinter e persistência local em SQLite.

O sistema permite cadastrar receitas e despesas, visualizar um dashboard financeiro simples e acompanhar todas as transações em uma tabela interativa.

## Tecnologias Utilizadas

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-green)
![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey)
![PyInstaller](https://img.shields.io/badge/Build-PyInstaller-purple)
![Inno Setup](https://img.shields.io/badge/Installer-Inno%20Setup-orange)
![Jenkins](https://img.shields.io/badge/CI%2FCD-Jenkins-red)

- **Python 3.10+**
- **Tkinter** para interface gráfica desktop
- **SQLite** com a biblioteca nativa `sqlite3`
- **PyInstaller** para gerar o executável Windows
- **Inno Setup** para gerar o instalador `.exe`
- **Jenkins Pipeline** para automatizar validação, build e empacotamento

## Arquitetura do Projeto

```text
.
├── finance_app/
│   ├── main.py
│   ├── database.py
│   ├── models/
│   │   └── transaction.py
│   ├── repositories/
│   │   └── transaction_repo.py
│   └── views/
│       └── main_window.py
│
├── installer/
│   └── setup.iss
│
├── Jenkinsfile
├── requirements.txt
├── .gitignore
└── README.md
```

### Organização das Camadas

- **`finance_app/main.py`**: ponto de entrada da aplicação. Inicializa o banco de dados, cria o repositório e abre a janela principal.
- **`finance_app/database.py`**: centraliza a conexão com o SQLite e a criação automática das tabelas necessárias.
- **`finance_app/models/`**: contém as entidades do domínio, como a classe `Transaction`, que representa uma transação financeira.
- **`finance_app/repositories/`**: concentra as operações de acesso a dados, como criação, listagem, exclusão e cálculo de resumo financeiro.
- **`finance_app/views/`**: contém a interface gráfica, mantendo a camada visual separada das regras de negócio e das queries SQL.
- **`installer/setup.iss`**: script do Inno Setup responsável por transformar o executável gerado pelo PyInstaller em um instalador Windows.
- **`Jenkinsfile`**: pipeline declarativa do Jenkins para validar o código, gerar o executável e arquivar o instalador.

Essa divisão facilita manutenção, testes futuros e evolução do projeto, evitando que interface, persistência e lógica fiquem misturadas no mesmo arquivo.

## Pré-requisitos

Para executar a aplicação em modo desenvolvimento:

- **Python 3.10 ou superior**
- **Tkinter disponível no ambiente Python**

Na maioria das instalações do Python, o Tkinter já vem incluído. Em algumas distribuições Linux, pode ser necessário instalar o pacote do sistema:

```bash
sudo apt install python3-tk
```

Para gerar o instalador Windows localmente ou via Jenkins:

- **Windows** no ambiente de build
- **Git**
- **Python 3.10+** disponível no `PATH`
- **Inno Setup 6**
- Acesso à internet para instalar o **PyInstaller** durante o build

## Instalação e Execução

### 1. Obter o projeto

Clone o repositório ou crie a estrutura de pastas do projeto localmente:

```bash
git clone <url-do-repositorio>
cd <nome-do-repositorio>
```

### 2. Criar um ambiente virtual

No Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No Windows:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

O projeto usa apenas bibliotecas nativas em tempo de execução. Mesmo assim, execute o comando abaixo para manter o fluxo padrão:

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

Em desenvolvimento, o arquivo local é gerado em:

```text
finance_app/finance_app.db
```

Quando a aplicação roda empacotada como executável, o banco é salvo em uma pasta gravável do usuário. No Windows, o caminho padrão é:

```text
%LOCALAPPDATA%\Finkado\finance_app.db
```

Isso evita problemas de permissão quando o aplicativo é instalado em uma pasta protegida do sistema.

## Build Local para Windows

O build local usa o mesmo fluxo automatizado no Jenkins: PyInstaller primeiro, Inno Setup depois.

Execute os comandos abaixo no PowerShell, a partir da raiz do projeto:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip install --upgrade pyinstaller
.\.venv\Scripts\python.exe -m PyInstaller --noconfirm --clean --onedir --windowed --name Finkado finance_app\main.py
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" installer\setup.iss
```

Após a execução, o instalador será gerado em:

```text
build_output/FinkadoSetup-1.0.0.exe
```

## Pipeline Jenkins com Inno Setup

A configuração deste projeto segue a mesma ideia do repositório de exemplo [InformaWendel/Jenkins](https://github.com/InformaWendel/Jenkins): o Jenkins obtém o código no GitHub, executa o build, chama o compilador do Inno Setup e arquiva o instalador final como artefato do build.

Neste projeto Python, o fluxo fica assim:

```text
GitHub
  → Jenkins
  → criar venv
  → instalar PyInstaller
  → validar código Python
  → gerar executável com PyInstaller
  → gerar instalador com Inno Setup
  → arquivar FinkadoSetup-1.0.0.exe
```

### 1. Preparar o agente Jenkins Windows

O agente Jenkins que executará a pipeline deve ter o label `windows`, ou você deve ajustar o bloco abaixo no `Jenkinsfile`:

```groovy
agent { label 'windows' }
```

Instale e valide as ferramentas no agente:

```powershell
python --version
git --version
& "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" /?
```

Se o Inno Setup estiver instalado em outro local, altere esta variável no `Jenkinsfile`:

```groovy
INNO_COMPILER = 'C:\\Program Files (x86)\\Inno Setup 6\\ISCC.exe'
```

### 2. Instalar plugins do Jenkins

Em **Manage Jenkins → Plugins**, confirme que os plugins abaixo estão instalados:

- **Pipeline**
- **Git plugin**
- **Pipeline: Stage View**
- **Workspace Cleanup**
- **Timestamper**
- **GitHub Branch Source** opcional, caso deseje usar webhooks ou pipelines multibranch

### 3. Publicar o projeto no GitHub

Se ainda não houver repositório remoto:

```bash
git init
git add .
git commit -m "feat: gestor financeiro com pipeline jenkins"
git branch -M main
git remote add origin https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git
git push -u origin main
```

### 4. Criar o job no Jenkins

1. Acesse o Jenkins.
2. Clique em **New Item**.
3. Informe um nome, por exemplo `finkado-pipeline`.
4. Escolha **Pipeline** e clique em **OK**.
5. Em **Pipeline**, configure:
   - **Definition**: `Pipeline script from SCM`
   - **SCM**: `Git`
   - **Repository URL**: `https://github.com/SEU_USUARIO/SEU_REPOSITORIO.git`
   - **Credentials**: informe uma credencial se o repositório for privado
   - **Branch Specifier**: `*/main`
   - **Script Path**: `Jenkinsfile`
6. Clique em **Save**.
7. Clique em **Build Now**.

### 5. O que a pipeline executa

O `Jenkinsfile` possui os seguintes estágios:

- **Checkout**: baixa o código-fonte do repositório.
- **Validate Tools**: confirma se `python`, `git` e `ISCC.exe` estão disponíveis no agente.
- **Prepare Python Environment**: cria a `.venv`, atualiza o `pip`, instala `requirements.txt` e instala o `pyinstaller`.
- **Validate Python Code**: executa `python -m compileall finance_app`.
- **Build Executable**: gera `dist/Finkado/Finkado.exe` com PyInstaller.
- **Package Installer**: executa `installer/setup.iss` com o compilador do Inno Setup.
- **Archive Installer**: publica `build_output/*.exe` como artefato baixável no Jenkins.

Ao final de uma build bem-sucedida, baixe o instalador em **Build → Artifacts**.

### 6. Webhook opcional no GitHub

Para disparar a pipeline automaticamente a cada push:

1. No GitHub, acesse **Settings → Webhooks → Add webhook**.
2. Configure:
   - **Payload URL**: `http://SEU_JENKINS/github-webhook/`
   - **Content type**: `application/json`
   - **Events**: `Just the push event`
3. No job do Jenkins, habilite **Build Triggers → GitHub hook trigger for GITScm polling**.

Se o Jenkins não estiver exposto para a internet, use **Poll SCM** como alternativa, por exemplo:

```text
H/5 * * * *
```

### 7. Versionamento de releases

Para gerar uma nova versão do instalador:

1. Atualize `APP_VERSION` em `Jenkinsfile`.
2. Atualize `MyAppVersion` em `installer/setup.iss`.
3. Faça commit e push.
4. Execute a pipeline novamente.

O instalador final seguirá o padrão:

```text
FinkadoSetup-<versao>.exe
```

### 8. Troubleshooting comum

| Sintoma | Causa provável | Solução |
| --- | --- | --- |
| `python` não é reconhecido | Python não está no `PATH` do agente Jenkins | Instale o Python e marque a opção de adicionar ao `PATH`, ou ajuste o ambiente do serviço Jenkins |
| `ISCC.exe não encontrado` | Inno Setup instalado em outro caminho | Atualize `INNO_COMPILER` no `Jenkinsfile` |
| `cleanWs` não existe | Plugin Workspace Cleanup ausente | Instale o plugin **Workspace Cleanup** ou remova o bloco `cleanWs` do `post` |
| PyInstaller não instala | Agente sem internet ou com proxy | Configure proxy no Jenkins/agente ou use um cache interno de pacotes |
| `Executável não gerado` | Entrada Python ou nome do app divergente | Confirme `PYTHON_ENTRY = 'finance_app\\main.py'` e `APP_NAME = 'Finkado'` |
| Inno Setup falha por arquivos ausentes | A pasta `dist/Finkado` não foi criada | Verifique o estágio **Build Executable** antes do estágio **Package Installer** |

## Referências

- [Repositório de exemplo InformaWendel/Jenkins](https://github.com/InformaWendel/Jenkins)
- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/syntax/)
- [PyInstaller Usage](https://pyinstaller.org/en/stable/usage.html)
- [Inno Setup](https://jrsoftware.org/isinfo.php)

