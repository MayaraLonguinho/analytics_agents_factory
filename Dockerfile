FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar apenas a estrutura exigida da arquitetura (AAF Modular Monolith)
COPY a_platform/ a_platform/
COPY b_documentation/ b_documentation/
COPY c_tests/ c_tests/
COPY d_input/ d_input/
COPY .agents/ .agents/
COPY .obsidian/ .obsidian/

# Copiar contrato publico do ambiente
COPY .env.example .env

# Criar pasta vazia garantida pelo .gitignore para os projetos gerados no container
RUN mkdir -p e_generated_projects

# Iniciar o AAF pelo entrypoint real da CLI
ENTRYPOINT ["python", "-m", "a_platform.b_interfaces.b_cli.b_cli"]
CMD ["--help"]
