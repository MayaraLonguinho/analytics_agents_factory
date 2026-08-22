import os
import sys
import subprocess

class RuntimeEngine:
    def execute_real(self, project_dir: str) -> bool:
        """
        Executa fisicamente o projeto:
        1. Cria venv na pasta
        2. Instala requirements.txt (se existir)
        3. Roda script main (se existir)
        4. Retorna True se tudo ocorrer bem.
        O pytest fica sob responsabilidade do ValidationGate, mas podemos rodar os scripts de infra/etl aqui.
        """
        if not os.path.exists(project_dir):
            return False
            
        print(f"  [Runtime] Acessando diretório: {project_dir}")
        venv_dir = os.path.join(project_dir, ".venv")
        
        # 1. Cria venv
        print(f"  [Runtime] Criando venv...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], cwd=project_dir, check=True, capture_output=True)
        
        # Determine python executable in venv
        if os.name == 'nt':
            venv_python = os.path.join(venv_dir, "Scripts", "python.exe")
            venv_pip = os.path.join(venv_dir, "Scripts", "pip.exe")
        else:
            venv_python = os.path.join(venv_dir, "bin", "python")
            venv_pip = os.path.join(venv_dir, "bin", "pip")
            
        # 2. Instala dependencias
        req_path = os.path.join(project_dir, "requirements.txt")
        if os.path.exists(req_path):
            print(f"  [Runtime] Instalando requirements...")
            try:
                subprocess.run([venv_pip, "install", "-r", "requirements.txt"], cwd=project_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"  [Runtime] Erro no pip install: {e.stderr.decode('utf-8')}")
                return False
                
        # 3. Roda script principal
        main_path = os.path.join(project_dir, "main.py")
        if os.path.exists(main_path):
            print(f"  [Runtime] Executando main.py...")
            try:
                subprocess.run([venv_python, "main.py"], cwd=project_dir, check=True, capture_output=True)
            except subprocess.CalledProcessError as e:
                print(f"  [Runtime] Erro no script principal: {e.stderr.decode('utf-8')}")
                return False
                
        return True
