from __future__ import annotations

from abc import ABC, abstractmethod
from numbers import Number
from sim.render import Renderer
from sim.util.vector import Vector3

from typing import TYPE_CHECKING
if TYPE_CHECKING:
	from sim.simulation import Simulation

class Entity(ABC):
	size:Number
	color:str
	marker:str = 'o'
	alpha:Number = 1
	
	pos:Vector3

	id_:int
	
	def create(self, sim:Simulation):
		self.sim = sim
	
	def remove(self):
		self.sim.remove_entity(self)

	@abstractmethod
	def tick(self, delta_t:Number, time:Number):
		...
	
	def draw(self, display:Renderer, time:Number)->None:
		display.axis.plot(
			*self.pos,
			marker=self.marker,
			markersize=self.size,
			color=self.color,
			alpha=self.alpha
		)
