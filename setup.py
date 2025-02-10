import os
import subprocess
import sys

def install_packages():
    """Install required packages."""
    print("Instalando pacotes do Python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Pacotes do Python instalados com sucesso.")

def install_nodejs_packages():
    """Install required Node.js packages."""
    print("Instalando pacotes do Node.js...")
    subprocess.check_call(["npm", "install"])
    print("Pacotes do Node.js instalados com sucesso.")

def setup_environment():
    """Setup the environment."""
    print("Configurando o ambiente...")

    # Setup Python environment
    install_packages()

    # Setup Node.js environment
    install_nodejs_packages()

    print("Ambiente configurado com sucesso.")

def main():
    """Main entry point."""
    try:
        setup_environment()
    except Exception as e:
        print(f"Ocorreu um erro durante a configuração: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
