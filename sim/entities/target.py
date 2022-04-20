from numbers import Number

from sim.util.vector import Vector3

from . import Entity


class Target(Entity):
	'''
	A simple entity used for representing a missile's target. By default, this
	draws an X on the canvas to denote the location. 
	'''
	def __init__(
		self, pos:Vector3, color:str='red', marker:str='x', size:Number=10
	):
		self.pos = pos
		self.color = color
		self.marker = marker
		self.size = size
	
	def tick(self, *_):
		...