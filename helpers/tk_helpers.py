import tkinter as tk
from helpers.functions import read_config, assess_options, bot_shoot
from ctypes import windll
windll.shcore.SetProcessDpiAwareness(1)
from PIL import Image, ImageTk 
import os
from tkinter import ttk



class App(tk.Tk):

    def load_image(self, path, size):
        # load and resize images per need
        img = Image.open(path)
        img = img.resize((size, size))
        img = ImageTk.PhotoImage(img)
        return img
        
    def set_window_geometry(self):
        # get the screen dimension
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # find the center point and set window geometry
        window_width = int(self.gui_config["window_width"])
        window_height = int(self.gui_config["window_height"])
        center_x = int(screen_width/2 -  window_width/2)
        center_y = int(screen_height/2 -  window_height/2)
        self.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    def set_window_title(self):
        # set window title
        window_title = self.gui_config["window_title"]
        self.title(window_title)

    def set_window_resize_option(self):
        # resize height and width
        resize_width = self.gui_config["resize_width"]
        resize_title = self.gui_config["resize_height"]
        self.resizable(resize_width, resize_title)

    def set_window_position(self):
        # open window on the top most postiton
        self.attributes('-topmost', 1)

    def set_window_icon(self):
        # setup the app icon
        icon_path = self.gui_config["icon_path"]
        self.iconbitmap(icon_path)

    def show_result_labels(self):
        # show appropriate label as per results
        user_result_img = getattr(self, self.user_result)
        if not hasattr(self, "user_result_lbl"):
            self.user_result_lbl = tk.Label(self, image = user_result_img)
            self.user_result_lbl.image = user_result_img
            self.user_result_lbl.place(relx = self.gui_config["lbl_relx_user"], rely = self.gui_config["lbl_rely_user"], anchor = 'center')
        else:
            self.user_result_lbl.configure(image = user_result_img)
            self.user_result_lbl.image = user_result_img

        bot_result_img = getattr(self, self.bot_result)
        if not hasattr(self, "bot_result_lbl"):
            self.bot_result_lbl = tk.Label(self, image = bot_result_img)
            self.bot_result_lbl.image = bot_result_img
            self.bot_result_lbl.place(relx = self.gui_config["lbl_relx_bot"], rely = self.gui_config["lbl_rely_bot"], anchor = 'center')
        else:
            self.bot_result_lbl.configure(image = bot_result_img)
            self.bot_result_lbl.image = bot_result_img

    def user_shoot(self, user_option):
        # compute the boot shoot option, assess the user vs boot shoot and show result on labels 
        bot_option = bot_shoot()
        self.user_result, self.bot_result = assess_options(user_option, bot_option)
        self.show_result_labels()

    def show_buttons(self):
        # setup buttons
        self.rock_btn = tk.Button(self, image = self.rock_img, borderwidth = 0, command=lambda: self.user_shoot(self.rock))
        self.rock_btn.place(relx = self.gui_config["btn_relx_rock"], rely = self.gui_config["btn_rely_rock"], anchor = 'center')

        self.paper_btn = tk.Button(self, image = self.paper_img, borderwidth = 0, command=lambda: self.user_shoot(self.paper))
        self.paper_btn.place(relx = self.gui_config["btn_relx_paper"], rely = self.gui_config["btn_rely_paper"], anchor = 'center')

        self.scissor_btn = tk.Button(self, image = self.scissor_img, borderwidth = 0, command=lambda: self.user_shoot(self.scissor))
        self.scissor_btn.place(relx = self.gui_config["btn_relx_scissor"], rely = self.gui_config["btn_rely_scissor"], anchor = 'center')

    def __init__(self):

        super().__init__()

        self.rock = "Rock"
        self.paper = "Paper"
        self.scissor = "Scissor"
        
        # read config
        self.gui_config = dict(read_config()).get("GUI")

        # import label images
        self.lbl_img_size = int(self.gui_config["lbl_img_size"])
        self.rock_loss_img = self.load_image(self.gui_config["rock_loss_img_path"], self.lbl_img_size)
        self.rock_win_img = self.load_image(self.gui_config["rock_win_img_path"], self.lbl_img_size)
        self.paper_loss_img = self.load_image(self.gui_config["paper_loss_img_path"], self.lbl_img_size)
        self.paper_win_img = self.load_image(self.gui_config["paper_win_img_path"], self.lbl_img_size)
        self.scissor_loss_img = self.load_image(self.gui_config["scissor_loss_img_path"], self.lbl_img_size)
        self.scissor_win_img = self.load_image(self.gui_config["scissor_win_img_path"], self.lbl_img_size)

        # import button images
        self.btn_img_size = int(self.gui_config["btn_img_size"])
        self.rock_img = self.load_image(self.gui_config["rock_img_path"], self.btn_img_size)
        self.paper_img = self.load_image(self.gui_config["paper_img_path"], self.btn_img_size)
        self.scissor_img = self.load_image(self.gui_config["scissor_img_path"], self.btn_img_size)


    def run(self):

        # set GUI window
        self.set_window_geometry()
        self.set_window_title()
        self.set_window_resize_option()
        self.set_window_position()
        self.set_window_icon()

        # set GUI widgets
        self.show_buttons()

        # run program
        self.mainloop()