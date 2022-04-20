from abc import ABC, abstractmethod
from numbers import Number
from sim.render import Renderer
from sim.util.vector import Vector3


class Entity(ABC):
	size:Number
	color:str
	marker:str = 'o'
	
	pos:Vector3
	
	@abstractmethod
	def tick(self, delta_t:Number, time:Number):
		...
	
	def draw(self, display:Renderer, time:Number)->None:
		display.axis.plot(
			*self.pos,
			marker=self.marker,
			markersize=self.size,
			color=self.color
		)
