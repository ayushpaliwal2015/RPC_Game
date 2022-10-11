import configparser

config_file_path = "./config.ini"

RPC_GAME_RULES = {
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
def assess_options(user_option, bot_option, USER_SCORE, BOT_SCORE):

    winner_option = RPC_GAME_RULES.get(str({user_option, bot_option}))
    if user_option == winner_option and bot_option == winner_option:
        USER_SCORE += 1; BOT_SCORE += 1
        return winner_option.lower() + "_win_img", winner_option.lower() + "_win_img", USER_SCORE, BOT_SCORE

    elif user_option == winner_option:
        USER_SCORE += 1
        return user_option.lower() + "_win_img", bot_option.lower() + "_loss_img", USER_SCORE, BOT_SCORE

    else:
        BOT_SCORE += 1
        return user_option.lower() + "_loss_img", bot_option.lower() + "_win_img", USER_SCORE, BOT_SCORE

def bot_shoot():
    return "Scissor"