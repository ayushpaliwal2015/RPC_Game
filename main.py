## Create Virtaul Env       ## python -m venv /path/to/venv
## Activate Virtual Env     ## path/to/venv/Scripts/activate    ## C:/users/ayush/venv/Scripts/activate
## Upgrade pip              ## pip install --upgrade pip
## Install dependencies     ## pip install -r requirements.txt

from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from helpers.tk_helpers import App

if __name__ == '__main__':
    app = App()
    app.run()