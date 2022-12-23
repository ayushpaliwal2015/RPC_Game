import tkinter as tk
from helpers.functions import read_config
from ctypes import windll
from PIL import Image, ImageTk 
import os
from agents.agents import Agents
from helpers.functions import calculate_window_geometry


windll.shcore.SetProcessDpiAwareness(1)

RPC_ENC  = {"rock": 0, "paper": 1, "scissor": 2}

RPC_GAME_RULES = {
    str({"rock", "paper"}): "paper",
    str({"rock", "rock"}) : "rock",
    str({"rock", "scissor"}): "rock",
    str({"paper", "paper"}): "paper",
    str({"scissor", "paper"}): "scissor",
    str({"scissor", "scissor"}): "scissor"
}

class App(tk.Tk, Agents):

    def load_image(self, path, size = None, img_resize_factor = None):
        # load and resize images per need
        img = Image.open(path)
        if not img_resize_factor:
            img = img.resize((size, size))
        else:
            width, height = img.size
            width = int(width * img_resize_factor)
            height = int(height * img_resize_factor)
            img = img.resize((width, height))
        img = ImageTk.PhotoImage(img)
        return img
        

    def set_window_geometry(self, window_name):
        # get the screen dimension
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()

        window_geometry = calculate_window_geometry(self.gui_config, window_name, self.screen_width, self.screen_height)
        self.geometry(window_geometry)

    def set_window_title(self):
        # set main window title
        window_title = self.gui_config["window_title"]
        self.title(window_title)

    def set_window_resize_option(self, window_name):
        # resize height and width of main window
        resize_width = self.gui_config[window_name + "_resize_width"]
        resize_title = self.gui_config[window_name + "_resize_height"]
        self.resizable(resize_width, resize_title)

    def set_window_position(self):
        # open main window on the top most postiton
        self.attributes('-topmost', 0)

    def set_window_icon(self):
        # setup the app icon
        icon_path = self.gui_config["icon_path"]
        self.iconbitmap(icon_path)

    def show_result_labels(self):
        # show appropriate label as per results
        user_result_img = getattr(self, self.user_result)
        self.user_result_lbl.configure(image = user_result_img)
        self.user_result_lbl.image = user_result_img

        bot_result_img = getattr(self, self.bot_result)
        self.bot_result_lbl.configure(image = bot_result_img)
        self.bot_result_lbl.image = bot_result_img

    def reset_scores(self):
        self.BOT_SCORE = 0
        self.USER_SCORE = 0

    def update_button_status(self, status):
        self.rock_btn.config(state = status)
        self.paper_btn.config(state = status)
        self.scissor_btn.config(state = status)

    def update_score_labels(self):
        # update bot and user score labels
        user_score_img = getattr(self, "score_" + str(self.USER_SCORE) + "_img")
        self.user_score_lbl.configure(image = user_score_img)
        self.user_score_lbl.image = user_score_img
        self.user_score_lbl.place(relx = self.gui_config["lbl_relx_user_score"], rely = self.gui_config["lbl_rely_user_score"], anchor = 'center')

        bot_score_img = getattr(self, "score_" + str(self.BOT_SCORE) + "_img")
        self.bot_score_lbl.configure(image = bot_score_img)
        self.bot_score_lbl.image = bot_score_img
        self.bot_score_lbl.place(relx = self.gui_config["lbl_relx_bot_score"], rely = self.gui_config["lbl_rely_bot_score"], anchor = 'center')


    def reset_avatars(self):
        # update bot and user avatar
        self.user_result_lbl.configure(image = self.user_img)
        self.user_result_lbl.image = self.user_img
        self.user_score_lbl.place(relx = self.gui_config["lbl_relx_user"], rely = self.gui_config["lbl_rely_user"], anchor = 'center')

        self.bot_result_lbl.configure(image = self.bot_img)
        self.bot_result_lbl.image = self.bot_img
        self.bot_score_lbl.place(relx = self.gui_config["lbl_relx_bot"], rely = self.gui_config["lbl_rely_bot"], anchor = 'center')


    # function to assess the result and return the corresponding labels
    def assess_options(self, user_option, bot_option):

        winner_option = RPC_GAME_RULES.get(str({user_option, bot_option}))
        if user_option == winner_option and bot_option == winner_option:
            self.USER_SCORE += 1; self.BOT_SCORE += 1; history = 1
            return winner_option + "_win_img", winner_option + "_win_img", self.USER_SCORE, self.BOT_SCORE, history

        elif user_option == winner_option:
            self.USER_SCORE += 1; history = 0
            return user_option + "_win_img", bot_option + "_loss_img", self.USER_SCORE, self.BOT_SCORE, history

        else:
            self.BOT_SCORE += 1; history = 2
            return user_option + "_loss_img", bot_option + "_win_img", self.USER_SCORE, self.BOT_SCORE, history

    # collect the bot and user shoot option and the result 
    def update_play_history(self, user_option, bot_option, history):
        self.agent_history.append(RPC_ENC.get(bot_option))
        self.player_history.append(RPC_ENC.get(user_option))
        self.win_history.append(history)

    def user_shoot(self, user_option):
        # compute the boot shoot option, assess the user vs boot shoot and show result on labels 
        bot_option = self.bot_shoot()
        self.user_result, self.bot_result, self.USER_SCORE, self.BOT_SCORE, history = self.assess_options(user_option, bot_option)
        self.show_result_labels()
        self.update_score_labels()

        # update history
        self.update_play_history(user_option, bot_option, history)

        # reset or close the app when max score is reached
        max_score = int(self.gui_config["max_score"])
        if self.USER_SCORE == max_score or self.BOT_SCORE == max_score:
            self.update_button_status(tk.DISABLED)
            self.generate_pop_up_window()

    def add_rpc_buttons(self):
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

    def init_score_lables(self):
        # setup user score label to 0
        self.user_score_lbl = tk.Label(self, image = self.score_0_img)
        self.user_score_lbl.image = self.score_0_img
        self.user_score_lbl.place(relx = self.gui_config["lbl_relx_user_score"], rely = self.gui_config["lbl_rely_user_score"], anchor = 'center')

        # setup bot score label to 0
        self.bot_score_lbl = tk.Label(self, image = self.score_0_img)
        self.bot_score_lbl.image = self.score_0_img
        self.bot_score_lbl.place(relx = self.gui_config["lbl_relx_bot_score"], rely = self.gui_config["lbl_rely_bot_score"], anchor = 'center')

    def init_bot_labels(self):
        # setup bot icon on window 
        self.user_img = self.load_image(self.gui_config["user_img"], img_resize_factor = float(self.gui_config["avtr_img_resize_factor"]))
        self.user_result_lbl = tk.Label(self, image = self.user_img)
        self.user_result_lbl.image = self.user_img
        self.user_result_lbl.place(relx = self.gui_config["lbl_relx_user"], rely = self.gui_config["lbl_rely_user"], anchor = 'center')

        # setup user icon on window 
        self.bot_img = self.load_image(self.gui_config["bot_img"], img_resize_factor = float(self.gui_config["avtr_img_resize_factor"]))
        self.bot_result_lbl = tk.Label(self, image = self.bot_img)
        self.bot_result_lbl.image = self.bot_img
        self.bot_result_lbl.place(relx = self.gui_config["lbl_relx_bot"], rely = self.gui_config["lbl_rely_bot"], anchor = 'center')


    def init_naming_labels(self):
        # setup user and bot labels on window
        self.bot_lbl = tk.Label(self, text = "BOT", font = ("Segoe UI", 10, "bold"))
        self.bot_lbl.place(relx = self.gui_config["lbl_relx_bot_name"], rely = self.gui_config["lbl_rely_bot_name"], anchor = 'center')

        self.user_lbl = tk.Label(self, text = "YOU", font = ("Segoe UI", 10, "bold"))
        self.user_lbl.place(relx = self.gui_config["lbl_relx_you_name"], rely = self.gui_config["lbl_rely_you_name"], anchor = 'center')

    def __init__(self):

        tk.Tk.__init__(self)
        Agents.__init__(self)

        self.rock = "rock"
        self.paper = "paper"
        self.scissor = "scissor"
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

        # initialize score labels to zero
        self.init_score_lables()

        # initialize bot labels
        self.init_bot_labels()

        # initialize name labels
        self.init_naming_labels()



    # set GUI window
    def setup_main_gui(self, window_name):
        
        self.set_window_geometry(window_name)
        self.set_window_title()
        self.set_window_resize_option(window_name)
        self.set_window_position()
        self.set_window_icon()

    def run(self):
        # set GUI main window
        self.setup_main_gui("main")

        # set GUI widgets
        self.add_rpc_buttons()

        # run program
        self.mainloop()

    def setup_pop_gui(self, window_name):
        
        # get the screen dimension
        window_geometry = calculate_window_geometry(self.gui_config, window_name, self.screen_width, self.screen_height)
        self.pop_up_window.geometry(window_geometry)

        # set pop window title
        window_title = self.gui_config["window_title"]
        self.pop_up_window.title(window_title)

        # resize height and width of pop window
        resize_width = self.gui_config[window_name + "_resize_width"]
        resize_title = self.gui_config[window_name + "_resize_height"]
        self.pop_up_window.resizable(resize_width, resize_title)

        # open pop window on the top most postiton
        self.pop_up_window.attributes('-topmost', 1)

        # setup the app icon
        icon_path = self.gui_config["icon_path"]
        self.pop_up_window.iconbitmap(icon_path)

        # close App if pop up window is closed
        self.pop_up_window.protocol('WM_DELETE_WINDOW', lambda: self.destroy())

        # open the window on the top most position
        self.pop_up_window.attributes('-topmost', 0)

    def reset_game(self):
        self.reset_scores()
        self.update_button_status(tk.NORMAL)
        self.pop_up_window.destroy()
        self.update_score_labels()
        self.reset_avatars()

    def add_pop_buttons(self):
        btn_height = int(self.gui_config["btn_height_pop"])
        btn_width = int(self.gui_config["btn_width_pop"])

        self.retry_btn = tk.Button(self.pop_up_window, text = "Yes", height = btn_height, width = btn_width, command = lambda: self.reset_game())
        self.retry_btn.place(relx = self.gui_config["btn_relx_retry"], rely = self.gui_config["btn_rely_retry"], anchor = 'center')

        self.close_btn = tk.Button(self.pop_up_window, text = "No", height = btn_height, width = btn_width, command = lambda: self.destroy())
        self.close_btn.place(relx = self.gui_config["btn_relx_close"], rely = self.gui_config["btn_rely_close"], anchor = 'center')

    def add_pop_labels(self):
        self.pop_lbl = tk.Label(self.pop_up_window, text = self.gui_config["lbl_text_pop"])
        self.pop_lbl.place(relx = self.gui_config["lbl_relx_pop"], rely = self.gui_config["lbl_rely_pop"], anchor = 'center')

    def generate_pop_up_window(self):

        self.pop_up_window = tk.Toplevel()
        self.setup_pop_gui("pop")
        self.add_pop_buttons()
        self.add_pop_labels()
