import configparser

config_file_path = "./config.ini"

# function to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config

# find the center point and set main window geometry
def calculate_window_geometry(gui_config, window_name, screen_width, screen_height):
    window_width = int(gui_config[window_name +  "_window_width"])
    window_height = int(gui_config[window_name + "_window_height"])
    center_x = int(screen_width/2 -  window_width/2)
    center_y = int(screen_height/2 -  window_height/2)
    return f'{window_width}x{window_height}+{center_x}+{center_y}'
