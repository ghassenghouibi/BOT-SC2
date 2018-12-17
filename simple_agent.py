from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features

"""--agent_race=F: value should be one of <R|P|T|Z>"""

"""python3 -m pysc2.bin.agent --map Simple64 --agent simple_agent.SimpleAgent --agent_race T"""



""" build a supply depot,and then a barracks and,then Extractor """

#Fonctions
_CONSTRUIRE_SUPPLYDEPOT=actions.FUNCTIONS.Build_SupplyDepot_screen.id
_RIENFAIRE=actions.FUNCTIONS.no_op.id


# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_COMMANDCENTER = 18
_TERRAN_SCV = 45

# Parameters
_PLAYER_SELF = 1
_NOT_QUEUED = [0]
_QUEUED = [1]



class SimpleAgent(base_agent.BaseAgent):
	"""Creer un simple Agent qui fait rien du tout"""
	base_top_left = None

	def step(self, obs):
		"""la deuxième variable est obs (observations) elle contient bcq de data 
		permet de connaitre c'est quoi les choses et ou ils sont situées"""
		super(SimpleAgent, self).step(obs)
		if self.base_top_left is None:
			player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
			self.base_top_left = player_y.mean() <= 31
		return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])