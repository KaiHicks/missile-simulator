from numbers import Number
from typing import Dict, Iterable

from tqdm import tqdm

from sim import Renderer
from sim.entities import Entity


class Simulation:
	display:Renderer
	entity_queue:Iterable[Entity]
	entities:Dict[int, Entity]
	
	_last_update:float|None
	_tps:Number
	
	def __init__(
		self, entities:Iterable[Entity], tps:Number=120
	):
		self.display = Renderer(self.draw, 512)
		self.entity_queue = entities
		self.entities = {}
		
		self._last_update = None
		self._tps = tps
	
	def run(self, time:Number=20, ticks:int=-1):
		'''
		Runs the simulation for the given time/ticks and stores the frame 
		information to be rendered later. If time and ticks are negative, then
		the simulation will run indefinitely. 
		'''
		if time == 0 or ticks == 0:
			# Run simulation for zero seconds or zero ticks
			return

		# Calculate the number of ticks we need
		if time < 0 and ticks < 0:
			# Make ticks large enough that it is basically infinite
			ticks = 2**31-1
		elif time > 0:
			ticks = int(time*self._tps)
		
		print(self.entities)
		# Main simulation loop
		for tick in tqdm(range(ticks), desc='Running simulation'):
			# tick the entities
			self.update(1/self._tps)
			# save to canvas
			self.display.refresh(tick/self._tps)
	
	def add_entity(self, e:Entity):
		self.entity_queue.append(e)

	def _flush_entity_queue(self):
		for entity in self.entity_queue:
			entity.create(self)
			self.entities[id(entity)] = entity
		self.entity_queue = []

	def remove_entity(self, e:Entity):
		self.entities.popitem(id(e))

	def show(self):
		'''
		Renders and plays the animation in a GUI
		'''
		self.display.show()
	
	def save(self, path:str='output.mp4'):
		'''
		Renders and exports the animation to the specified file path
		'''
		self.display.save(path=path)
	
	def draw(self):
		'''
		Draws all entities to the canvas
		'''
		for entity in self.entities.values():
			entity.draw(self.display, self._last_update)
	
	def update(self, delta_t=None):
		'''
		Ticks all entities
		'''
		self._flush_entity_queue()

		# Calculate the time delta if it wasn't given
		self._last_update = self._last_update or 0
		delta_t = delta_t or self._last_update + 1/self._tps
		
		for entity in self.entities.values():
			entity.tick(delta_t, self._last_update + delta_t)
			self._last_update += delta_t
