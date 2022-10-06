import configparser
import os.path
import os

config_file_path = "./config.ini"

# Method to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config