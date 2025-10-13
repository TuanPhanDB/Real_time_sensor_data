import subprocess
import os

def run_terminal(title, command):
    subprocess.Popen([
        "powershell",
        "-NoExit",
        f"-Command",
        f"$Host.UI.RawUI.WindowTitle = '{title}'; {command}"
    ],
    creationflags=subprocess.CREATE_NEW_CONSOLE)

if __name__ == "__main__":

    base_dir = os.path.join(os.getcwd(), "src")
    activate = ".\\env\\Scripts\\activate"

    #Terminal 1: data_generator.py
    cmd1 = f'Set-Location "{base_dir}"; {activate}; uvicorn data_generator:app --reload'
    
    #Terminal 2: producer.py
    cmd2 = f'Set-Location "{base_dir}"; {activate}; py producer.py'

    #Terminal 3: consumer.py
    cmd3 = f'Set-Location "{base_dir}"; {activate}; py consumer.py'

    print("Starting services....")
    run_terminal("Data generator", cmd1)
    run_terminal("Producer", cmd2)
    run_terminal("Consumer", cmd3)

    print("Services started")