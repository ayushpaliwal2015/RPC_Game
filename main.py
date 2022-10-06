## Create Virtaul Env       ## python -m venv /path/to/venv
## Activate Virtual Env     ## path/to/venv/Scripts/activate    ## C:/users/ayush/venv/Scripts/activate
## Upgrade pip              ## pip install --upgrade pip
## Install dependencies     ## pip install -r requirements.txt

import tkinter as tk
from helpers.config_parser import read_config
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from PIL import Image, ImageTk 
import os
from tkinter import ttk

# setup root tk instance
root = tk.Tk()

# read config
config = read_config()

# get the screen dimension
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# find the center point and set window geometry
window_width = int(config["GUI"]["window_width"])
window_height = int(config["GUI"]["window_height"])
center_x = int(screen_width/2 -  window_width/2)
center_y = int(screen_height/2 -  window_height/2)
root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

# set window title
window_title = config["GUI"]["window_title"]
root.title(window_title)

# resize height and width
resize_width = config["GUI"]["resize_width"]
resize_title = config["GUI"]["resize_height"]
root.resizable(resize_width, resize_title)

# open window on the top most postiton
root.attributes('-topmost', 1)

# setup the app icon
icon_path = config["GUI"]["icon_path"]
root.iconbitmap(icon_path)

###############
def user_input(option):
    print(option)
###############

# import button images
resize_factor = float(config["GUI"]["btn_img_resize_factor"])

rock_img = Image.open(config["GUI"]["rock_img_path"])
rock_img = rock_img.resize((round(rock_img.size[0]*resize_factor), round(rock_img.size[1]*resize_factor)))
rock_img = ImageTk.PhotoImage(rock_img)

paper_img = Image.open(config["GUI"]["paper_img_path"])
paper_img = paper_img.resize((round(paper_img.size[0]*resize_factor), round(paper_img.size[1]*resize_factor)))
paper_img = ImageTk.PhotoImage(paper_img)

scissor_img = Image.open(config["GUI"]["scissor_img_path"])
scissor_img = scissor_img.resize((round(scissor_img.size[0]*resize_factor), round(scissor_img.size[1]*resize_factor)))
scissor_img = ImageTk.PhotoImage(scissor_img)

# setup buttons
tk.Button(root, text='Rock', image = rock_img, borderwidth = 0, command=lambda: user_input('Rock')).pack()
tk.Button(root, text='Paper', image = paper_img, borderwidth = 0, command=lambda: user_input('Paper')).pack()
tk.Button(root, text='Scissors', image = scissor_img, borderwidth = 0, command=lambda: user_input('Scissors')).pack()

root.mainloop()

