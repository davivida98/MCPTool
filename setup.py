import subprocess
import sys
import os

class Setup:
    hide_output = '>/dev/null 2>&1'
    python_variable = sys.executable
    nodejs_modules = ['express']

    @staticmethod
    def check_termux():
        return os.path.exists('/data/data/com.termux')

    @staticmethod
    def check_by_command(command):
        return subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0

    @staticmethod
    def ask(question):
        answer = input(question).lower().strip()
        return answer == 'y'

    @staticmethod
    def install_nodejs():
        if Setup.check_termux():
            subprocess.run('pkg install nodejs -y', shell=True)
        else:
            subprocess.run('sudo apt install nodejs -y', shell=True)
        print('\n[+] NodeJS installed successfully.')

    @staticmethod
    def install_java():
        if Setup.check_termux():
            subprocess.run('pkg install openjdk-17 -y', shell=True)
        else:
            subprocess.run('sudo apt install openjdk-17-jdk openjdk-17-jre -y', shell=True)
        print('\n[+] Java installed successfully.')

    @staticmethod
    def install_nmap():
        if Setup.check_termux():
            subprocess.run('pkg install nmap -y', shell=True)
        else:
            subprocess.run('sudo apt install nmap -y', shell=True)
        print('\n[+] Nmap installed successfully.')

    @staticmethod
    def install_ngrok():
        if Setup.check_termux():
            subprocess.run('pkg install wget -y', shell=True)
            subprocess.run('wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-arm.zip', shell=True)
            subprocess.run('unzip ngrok-stable-linux-arm.zip', shell=True)
        else:
            subprocess.run('curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list && sudo apt update && sudo apt install ngrok -y', shell=True)
        print('\n[+] Ngrok installed successfully.')

    @staticmethod
    def install_sox():
        subprocess.run(f'pkg install sox -y {Setup.hide_output}', shell=True)
        print('\n[+] Sox installed successfully.')

    @staticmethod
    def start_setup():
        """
        Verify and install the dependencies needed to use MCPTool.
        Also, prepare the configuration file for the user.
        """

        if Setup.check_termux():
            print('\n[+] Updating APT packages..')
            subprocess.run('apt update && apt upgrade -y', shell=True)

        print('\n[+] Installing the necessary python modules..')
        subprocess.run(f'{Setup.python_variable} -m pip install -r requirements.txt {Setup.hide_output}', shell=True)

        # NodeJS Check
        if not Setup.check_by_command(f'npm --version {Setup.hide_output}'):
            answer = Setup.ask('\n[-] NodeJS is not installed on the system. Do you want to install it automatically? y/n > ')
        
            if answer:
                print('\n[+] Installing NodeJS..')
                Setup.install_nodejs()
            else:
                print('\n[-] Install NodeJS and start the script again.')
                return
        
        print('\n[+] Installing NodeJS modules..')
