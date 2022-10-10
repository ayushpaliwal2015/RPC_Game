import configparser

config_file_path = "./config.ini"

rpc_game_rules = {
    str({"Rock", "Paper"}): "Paper",
    str({"Rock", "Rock"}) : "Rock",
    str({"Rock", "Scissor"}): "Rock",
    str({"Paper", "Paper"}): "Paper",
    str({"Scissor", "Paper"}): "Scissor",
    str({"Scissor", "Scissor"}): "Scissor"
}

# function to read config file settings
def read_config():
    config = configparser.ConfigParser()
    config.read(config_file_path)
    return config

# function to assess the result and return the corresponding labels
def assess_options(user_option, bot_option):
    winner_option = rpc_game_rules.get(str({user_option, bot_option}))

    if user_option == winner_option and bot_option == winner_option:
        return winner_option.lower() + "_win_img", winner_option.lower() + "_win_img"
    elif user_option == winner_option:
        return user_option.lower() + "_win_img", bot_option.lower() + "_loss_img"
    else:
        return user_option.lower() + "_loss_img", bot_option.lower() + "_win_img"

def bot_shoot():
    return "Scissor"