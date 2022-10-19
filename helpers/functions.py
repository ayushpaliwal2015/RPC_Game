import configparser

config_file_path = "./config.ini"

RPC_GAME_RULES = {
    str({"rock", "paper"}): "paper",
    str({"rock", "rock"}) : "rock",
    str({"rock", "scissor"}): "rock",
    str({"paper", "paper"}): "paper",
    str({"scissor", "paper"}): "scissor",
    str({"scissor", "scissor"}): "scissor"
}


# function to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config


