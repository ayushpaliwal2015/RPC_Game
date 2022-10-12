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

    def update_score_labels(self):
        # update bot and user score labels
        max_score = int(self.gui_config["max_score"])
        if self.USER_SCORE > max_score or self.BOT_SCORE > max_score:

            if self.USER_SCORE > max_score and self.BOT_SCORE > max_score:
                self.BOT_SCORE = 1
                self.USER_SCORE = 1

            elif self.USER_SCORE > max_score:
                self.USER_SCORE -= max_score
                self.BOT_SCORE = 0

            else:
                self.BOT_SCORE -= max_score
                self.USER_SCORE = 0

        user_score_img = getattr(self, "score_" + str(self.USER_SCORE) + "_img")
        self.user_score_lbl.configure(image = user_score_img)
        self.user_score_lbl.image = user_score_img

        bot_score_img = getattr(self, "score_" + str(self.BOT_SCORE) + "_img")
        self.bot_score_lbl.configure(image = bot_score_img)
        self.bot_score_lbl.image = bot_score_img

    def user_shoot(self, user_option):
        # compute the boot shoot option, assess the user vs boot shoot and show result on labels 
        bot_option = bot_shoot()
        self.user_result, self.bot_result, self.USER_SCORE, self.BOT_SCORE = assess_options(user_option, bot_option, self.USER_SCORE, self.BOT_SCORE)
        self.show_result_labels()
        self.update_score_labels()

    def show_buttons(self):
        # setup buttons
        self.rock_btn = tk.Button(self, image = self.rock_img, borderwidth = 0, command=lambda: self.user_shoot(self.rock))
        self.rock_btn.place(relx = self.gui_config["btn_relx_rock"], rely = self.gui_config["btn_rely_rock"], anchor = 'center')

        self.paper_btn = tk.Button(self, image = self.paper_img, borderwidth = 0, command=lambda: self.user_shoot(self.paper))
        self.paper_btn.place(relx = self.gui_config["btn_relx_paper"], rely = self.gui_config["btn_rely_paper"], anchor = 'center')

        self.scissor_btn = tk.Button(self, image = self.scissor_img, borderwidth = 0, command=lambda: self.user_shoot(self.scissor))
        self.scissor_btn.place(relx = self.gui_config["btn_relx_scissor"], rely = self.gui_config["btn_rely_scissor"], anchor = 'center')

    def import_result_lbl_img(self):
        # import shoot result label images
        self.result_lbl_img_size = int(self.gui_config["result_lbl_img_size"])
        for option in self.options:
            for result in self.results:
                attr = option + "_" + result + "_img"
                img = self.load_image(self.gui_config[attr + "_path"], self.result_lbl_img_size)
                setattr(self, attr, img)

    def import_btn_img(self):
        # import button images
        self.btn_img_size = int(self.gui_config["btn_img_size"])
        for option in self.options:
            attr = option + "_img"
            img = self.load_image(self.gui_config[attr + "_path"], self.btn_img_size)
            setattr(self, attr, img)

    def import_score_lbl_img(self):
        # import score label images   
        self.score_lbl_img_size = int(self.gui_config["score_lbl_img_size"])
        for score in map(str, range(int(self.gui_config["max_score"]) + 1)):
            attr = "score_" + score + "_img"
            img = self.load_image(self.gui_config[attr + "_path"], self.score_lbl_img_size)
            setattr(self, attr, img)

    def __init__(self):

        super().__init__()

        self.rock = "Rock"
        self.paper = "Paper"
        self.scissor = "Scissor"
        self.USER_SCORE = 0
        self.BOT_SCORE = 0
        self.options = ["rock", "paper", "scissor"]
        self.results = ["win", "loss"]
        
        # read config
        self.gui_config = dict(read_config()).get("GUI")

        # import label and button images
        self.import_result_lbl_img()
        self.import_btn_img()
        self.import_score_lbl_img()

        # setup user score label to 0
        self.user_score_lbl = tk.Label(self, image = self.score_0_img)
        self.user_score_lbl.image = self.score_0_img
        self.user_score_lbl.place(relx = self.gui_config["lbl_relx_user_score"], rely = self.gui_config["lbl_rely_user_score"], anchor = 'center')

        # setup bot score label to 0
        self.bot_score_lbl = tk.Label(self, image = self.score_0_img)
        self.bot_score_lbl.image = self.score_0_img
        self.bot_score_lbl.place(relx = self.gui_config["lbl_relx_bot_score"], rely = self.gui_config["lbl_rely_bot_score"], anchor = 'center')


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