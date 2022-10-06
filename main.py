## Create Virtaul Env       ## python -m venv /path/to/venv
## Activate Virtual Env     ## path/to/venv/Scripts/activate    ## C:/users/ayush/venv/Scripts/activate
## Upgrade pip              ## pip install --upgrade pip
## Install dependencies     ## pip install -r requirements.txt

import tkinter as tk
from helpers.config_parser import read_config
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
import os

# setup root tk instance
root = tk.Tk()

# read config
config = read_config()

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point and set window geometry
window_width = int(config["Front_End"]["window_width"])
window_height = int(config["Front_End"]["window_height"])
center_x = int(screen_width/2 -  window_width/2)
center_y = int(screen_height/2 -  window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# set window title
window_title = config["Front_End"]["window_title"]
root.title(window_title)

# resize height and width
resize_width = config["Front_End"]["resize_width"]
resize_title = config["Front_End"]["resize_height"]
root.resizable(resize_width, resize_title)

# open window on the top most postiton
root.attributes('-topmost', 1)

# setup the app icon
icon_path = config["Front_End"]["icon_path"]
root.iconbitmap(icon_path)


root.mainloop()

