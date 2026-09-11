# Instalação

## Pré-requisitos
- Python 3.10 ou superior
- Git

## Onde baixar
- [Python](https://www.python.org/downloads/)
- IDE Recomendada: Cursor, VS Code (com Claude Dev / Cline), ou Devin.

## Como verificar a instalação
Abra o terminal e execute:
```bash
python --version
# ou
python3 --version

pip --version
```

## Como abrir o projeto
Navegue até o diretório do projeto no seu terminal:
```bash
cd /caminho/para/analytics_agents_factory
```

## Ambiente Virtual
É altamente recomendado o uso de um ambiente virtual para isolar as dependências.

**Criação do ambiente virtual:**
```bash
python -m venv venv
```

**Ativação:**
- macOS/Linux:
```bash
source venv/bin/activate
```
- Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```
- Windows CMD:
```cmd
.\venv\Scripts\activate.bat
```

## Instalação de Dependências
Com o ambiente ativado, atualize o pip e instale as dependências:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Configuração de Credenciais
1. Duplique o arquivo `.env.example` e renomeie para `.env`.
2. Preencha as chaves de API dos provedores suportados:
```env
OPENAI_API_KEY=sua_chave_aqui
ANTHROPIC_API_KEY=sua_chave_aqui
GOOGLE_API_KEY=sua_chave_aqui
```
