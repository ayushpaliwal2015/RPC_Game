## Create Virtaul Env       ## python -m venv /path/to/venv
## Activate Virtual Env     ## path/to/venv/Scripts/activate    ## C:/users/ayush/venv/Scripts/activate
## Upgrade pip              ## pip install --upgrade pip
## Install dependencies     ## pip install -r requirements.txt
## If Python isn't on your Windows path, you may need to type out the full path to pyinstaller to get it to run.
## Build executable file    ## pyinstaller main.py --onefile --noconsole --icon=rpc_icon.ico

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from helpers.tk_helpers import App

if __name__ == '__main__':
    app = App()
    app.run()