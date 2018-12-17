from pysc2.agents import base_agent
from pysc2.lib import actions
from pysc2.lib import features


import time 
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

# Functions
_BUILD_BARRACKS = actions.FUNCTIONS.Build_Barracks_screen.id
_BUILD_SUPPLYDEPOT = actions.FUNCTIONS.Build_SupplyDepot_screen.id
_NOOP = actions.FUNCTIONS.no_op.id
_SELECT_POINT = actions.FUNCTIONS.select_point.id
_TRAIN_MARINE = actions.FUNCTIONS.Train_Marine_quick.id
_RALLY_UNITS_MINIMAP = actions.FUNCTIONS.Rally_Units_minimap.id
_SELECT_ARMY = actions.FUNCTIONS.select_army.id
_ATTACK_MINIMAP = actions.FUNCTIONS.Attack_minimap.id

# Features
_PLAYER_RELATIVE = features.SCREEN_FEATURES.player_relative.index
_UNIT_TYPE = features.SCREEN_FEATURES.unit_type.index

# Unit IDs
_TERRAN_BARRACKS = 21
_TERRAN_COMMANDCENTER = 18
_TERRAN_SUPPLYDEPOT = 19
_TERRAN_SCV = 45



class SimpleAgent(base_agent.BaseAgent):
	"""Creer un simple Agent qui fait rien du tout"""
	base_top_left = None
	supply_depot_built=False
	scv_selected=False
	
	def transformLocation(self, x, x_distance, y, y_distance):
		if not self.base_top_left:
			return [x - x_distance, y - y_distance]
        
		return [x + x_distance, y + y_distance]

	def SelectionnerUnSCV(self,obs):
		"""Fonction de selection d'un scv"""
		if not self.supply_depot_built:
			if not self.scv_selected:
				print("Selectionner un scv")
				unit_type = obs.observation["screen"][features.SCREEN_FEATURES.unit_type.index]
				unit_y,unit_x =(unit_type == 45).nonzero()
				target=[unit_x[0],unit_y[0]]
				self.scv_selected=True
				print("scv à était séléctionner",target)
				return actions.FunctionCall(actions.FUNCTIONS.select_point.id,[_NOT_QUEUED,target])

	def ConstruireSupplyDepot(self,obs):
		""""""
		if not self.supply_depot_built:
			print("Commencer à Bâtir le SupplyDepot")
			unit_type=obs.observation["screen"][features.SCREEN_FEATURES.unit_type.index]
			unit_y,unit_x=(unit_type == 18).nonzero()
			#print("Coordonnes ",unit_x,unit_y)
			target=self.transformLocation(int(unit_x.mean()),0,int(unit_y.mean()),20)
			print("Target ",target)
			self.supply_depot_built=True
			return actions.FunctionCall(actions.FUNCTIONS.Build_SupplyDepot_screen.id, [_NOT_QUEUED, target])


	def step(self, obs):
		"""La deuxième variable est obs (observations) elle contient bcq de data 
		permet de connaitre c'est quoi les choses et ou ils sont situées"""
		super(SimpleAgent, self).step(obs)
		time.sleep(0.5)
		if self.base_top_left is None:
			player_y, player_x = (obs.observation["minimap"][_PLAYER_RELATIVE] == _PLAYER_SELF).nonzero()
			self.base_top_left = player_y.mean() <= 31
		
		if not self.scv_selected:
			return self.SelectionnerUnSCV(obs)
		

		return actions.FunctionCall(actions.FUNCTIONS.no_op.id, [])