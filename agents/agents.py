import numpy as np
import json
from helpers.functions import read_config
from random import shuffle

RPC_REV_ENC = {0: "rock", 1: "paper", 2: "scissor"}
OPPONENT_ENC = {"agent": 2, "draw": 1, "player": 0}
OPPONENT_REV_ENC = {2: "agent", 1: "draw", 0: "player"}

# TODO: add comments in this module
class Agents:
  def __init__(self):

    # read config
    self.agent_config = dict(read_config()).get("AGENT")

    self.agent_history = []
    self.player_history = []
    self.win_history = []
    self.no_of_options = len(RPC_REV_ENC)
    self.round_no = 1
    self.agent_rounds_left = 0
    self.current_agent_index = -1

    self.no_of_agent_rounds = json.loads(self.agent_config.get("no_of_agent_rounds"))
    self.agent_rounds_probab = json.loads(self.agent_config.get("agent_rounds_probab"))
    self.first_n_random_rounds = int(self.agent_config.get("first_n_random_rounds"))
    self.no_of_agent_id_replications = int(self.agent_config.get("no_of_agent_id_replications"))

    self.agent_ids = json.loads(self.agent_config.get("agent_ids"))
    shuffle(self.agent_ids)
    self.agent_ids = self.agent_ids * self.no_of_agent_id_replications

  def generate_no_of_agent_rounds(self):
    self.agent_rounds_left = np.random.choice(self.no_of_agent_rounds, 1, p = self.agent_rounds_probab)[0]

  def bot_shoot(self):

    # throw random option for first n rounds
    if self.round_no <= self.first_n_random_rounds:
      bot_option = self.throw_agent_0()
      
    elif self.round_no == self.first_n_random_rounds + 1 or self.agent_rounds_left == 0:
      self.current_agent_index += 1
      self.current_agent = getattr(self, "throw_agent_" + str(self.agent_ids[self.current_agent_index]))
      bot_option = self.current_agent()

      self.generate_no_of_agent_rounds()
      self.agent_rounds_left -= 1

    else:
      bot_option = self.current_agent()
      self.agent_rounds_left -= 1

    self.round_no +=1
    bot_option = RPC_REV_ENC.get(bot_option)
    return bot_option

  def throw_agent_0(self):
    option = np.random.choice(self.no_of_options, 1)[0]
    return option

  def throw_agent_1(self):
    return 0

  def throw_agent_2(self):
    return 1

  def throw_agent_3(self):
    return 2