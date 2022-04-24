from abc import ABC
from collections import deque
from numbers import Number

import numpy as np

from sim import Entity, Renderer
from sim.entities.missile import Explosion
from sim.util import G, Vector3


class Missile(Entity, ABC):
	initial_pos:Vector3
	vel:Vector3
	mass:Number
	
	destroyed:bool
	
	_acc:Vector3
	
	def __init__(
		self, pos:Vector3, vel:Vector3, mass:Number=1, size:Number=None, 
		color:str='red', tail_color:str='orange', tail_len:int=150,
		explosion_size:Number=10
	):
		self.initial_pos = pos.copy()
		self.pos = pos
		self.vel = vel
		self.mass = mass
		self.size = size or self.mass
		self.explosion_size = explosion_size
		
		self.color = color
		self.tail_color = tail_color
		
		self.marker = 'o'
		self.destroy_marker = 'x'
		
		self.destroyed = False
		
		self._gravity = True
		self._acc = Vector3(0)
		
		self._tail = deque(maxlen=tail_len)
	
	def apply_accel(self, acceleration:Vector3)->None:
		self._acc += acceleration
	
	def apply_force(self, force:Vector3)->None:
		self.apply_accel(force/self.mass)
	
	def tick(self, delta_t:Number, time:Number)->None:
		# Manage tail
		self._tail.append(self.pos.copy())
		
		# Determine if destroyed
		if self.pos.z < 0:
			self.pos.z = 0
			self.destroyed = True
			self.detonate()
		if not self.destroyed:
			# Apply gravity
			if self._gravity:
				self.apply_accel(Vector3(0, 0, -G))
			
			# Apply acceleration
			self.pos += self.vel*delta_t + 1/2*self._acc*delta_t**2
			self.vel += self._acc*delta_t
			
			# Reset acceleration
			self._acc = Vector3(0)
	
	def detonate(self)->None:
		self.destroyed = True
		self.sim.add_entity(Explosion(self.pos))

	def draw(self, display:Renderer, time:Number)->None:
		display.axis.plot(
			*self.pos,
			marker=self.marker if not self.destroyed else self.destroy_marker,
			markersize=self.size,
			color=self.color
		)
		display.axis.plot(
			*np.column_stack(self._tail),
			color=self.tail_color
		)
