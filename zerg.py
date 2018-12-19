from pysc2.agents import base_agent
from pysc2.env import sc2_env
from pysc2.lib import actions,features,units
from absl import app
import sys,random

class ZergAgent(base_agent.BaseAgent):
	"""Construire un Agent de type Zerg"""
	def __init__(self):
		"""Fonction d'initialisation"""
		super(ZergAgent,self).__init__()
		self.attack_coordinates=None


	def selection(self,obs,unit_type):
		""" Séléction d'unités par groupe """
		if (len(obs.observation.single_select) > 0 and obs.observation.single_select[0].unit_type == unit_type):
			return True
    
		elif (len(obs.observation.multi_select) > 0 and obs.observation.multi_select[0].unit_type == unit_type):
			return True
		else:
			return False

	def obtenirtype(self,obs,unit_type):
		""" Extraire le type de l'unité """
		for unit in obs.observation.feature_units:
			if unit.unit_type == unit_type:
				return unit

	def get_units_by_type(self, obs, unit_type):
		""" Extraire le type de l'unité"""
		return [unit for unit in obs.observation.feature_units
	        if unit.unit_type == unit_type]
	

	def actionpossible(self,obs,action):
		""" Les coups possibles """
		return action in obs.observation.available_actions

	
	
	def step(self,obs):
		"""Les steps du jeu"""
		times=0
		super(ZergAgent,self).step(obs)
		if obs.first():
			_player_y,_player_x =(obs.observation.feature_minimap.player_relative == features.PlayerRelative.SELF).nonzero()
			_x_mean=_player_x.mean()
			_y_mean=_player_y.mean()
			if _x_mean <=31 and _y_mean <=31:
				self.attack_coordinates =(49,49)
			else:
				self.attack_coordinates =(12,16)
		

		#Evolution_chamber
		evolution_chamber=self.get_units_by_type(obs,units.Zerg.EvolutionChamber)
		if len(evolution_chamber) ==0:
			if self.selection(obs,units.Zerg.Drone):	
				if self.actionpossible(obs,actions.FUNCTIONS.Build_EvolutionChamber_screen.id):
					x=random.randint(0,83)
					y=random.randint(0,83)
					return actions.FUNCTIONS.Build_EvolutionChamber_screen("now",(x,y))
		

		#Exctractor
		exctractor=self.get_units_by_type(obs,units.Zerg.Extractor)
		if len(exctractor) == 0:
			if self.selection(obs,units.Zerg.Drone):
				if self.actionpossible(obs,actions.FUNCTIONS.Build_Extractor_screen.id):
					x=random.randint(0,83)
					y=random.randint(0,83)
					return actions.FUNCTIONS.Build_Extractor_screen("now",(x,y))

		#zerglings
		zerglings = self.get_units_by_type(obs,units.Zerg.Zergling)
		
		if len(zerglings) >= 9:
			if self.selection(obs,units.Zerg.Zergling):
				if self.actionpossible(obs,actions.FUNCTIONS.Attack_minimap.id):
					return actions.FUNCTIONS.Attack_minimap("now",self.attack_coordinates)
			if self.actionpossible(obs,actions.FUNCTIONS.select_army.id):
				return actions.FUNCTIONS.select_army("select")
		#spawning_pools
		spawning_pools=self.get_units_by_type(obs,units.Zerg.SpawningPool)
		if len(spawning_pools) == 0:
			if self.selection(obs,units.Zerg.Drone):
				if self.actionpossible(obs,actions.FUNCTIONS.Build_SpawningPool_screen.id):
					x=random.randint(0,83)
					y=random.randint(0,83)

					return actions.FUNCTIONS.Build_SpawningPool_screen("now",(x,y))
			drones = self.get_units_by_type(obs,units.Zerg.Drone)
			if len(drones)> 0:
				drone=random.choice(drones)
				return actions.FUNCTIONS.select_point("select_all_type",(drone.x,drone.y))
		
		#train zergling or overloard (Egg)
		if self.selection(obs,units.Zerg.Larva):
			free_supply=(obs.observation.player.food_cap - obs.observation.player.food_used)
			if free_supply ==0:
				if self.actionpossible(obs,actions.FUNCTIONS.Train_Overlord_quick.id):
					return actions.FUNCTIONS.Train_Overlord_quick("now")
			if self.actionpossible(obs,actions.FUNCTIONS.Train_Zergling_quick.id):
				return actions.FUNCTIONS.Train_Zergling_quick("now")

		#larvae
		larvae=self.get_units_by_type(obs,units.Zerg.Larva)
		if len(larvae) >0:
			larva=random.choice(larvae)
			return actions.FUNCTIONS.select_point("select_all_type",(larva.x,larva.y))
		


		#hatchery
		hatchery=self.get_units_by_type(obs,units.Zerg.Hatchery)
		if len(hatchery) < 2:
			if self.selection(obs,units.Zerg.Drone):	
				if self.actionpossible(obs,actions.FUNCTIONS.Build_Hatchery_screen.id):
					x=random.randint(0,83)
					y=random.randint(0,83)
					return actions.FUNCTIONS.Build_Hatchery_screen("now",(x,y))

			drones = self.get_units_by_type(obs,units.Zerg.Drone)
			if len(drones)> 0:
				drone=random.choice(drones)
				return actions.FUNCTIONS.select_point("select_all_type",(drone.x,drone.y))

		


		return actions.FUNCTIONS.no_op()



def main(unused_argv):
	"""main fonction initilisation de map,joueur,interface etc .."""
	agent=ZergAgent()
	try:
		while True:
			with sc2_env.SC2Env(
				map_name="Simple64",
				players=[sc2_env.Agent(sc2_env.Race.zerg),
						sc2_env.Bot(sc2_env.Race.random,
									sc2_env.Difficulty.medium)],
	          	agent_interface_format=features.AgentInterfaceFormat(
                	feature_dimensions=features.Dimensions(screen=84, minimap=64),
                	use_feature_units=True),
	          	step_mul=0,
	          	game_steps_per_episode=0,
				visualize=True) as env:
				agent.setup(env.observation_spec(),env.action_spec())
				timesteps=env.reset()
				agent.reset()

				while True:
					step_actions = [agent.step(timesteps[0])]
					if timesteps[0].last():
						sys.exit(0)
					timesteps=env.step(step_actions)
	except KeyboardInterrupt:
		pass

if __name__ =="__main__":
	app.run(main)
