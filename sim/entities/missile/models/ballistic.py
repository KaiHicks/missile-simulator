from numbers import Number
from typing import Tuple

import numpy as np
from sim.entities.missile.missile import Missile
from sim.render import Renderer
from sim.simulation import Simulation
from sim.util import G
from sim.util.vector import Vector3


class Ballistic(Missile):
	def __init__(
		self, pos:Vector3, burn_time:Number, launch_time:Number=2**31-1, 
		burn_acc:Number=5*G, mass:Number=1, size:Number=None, color:str='teal', 
		tail_color:str='teal'
	):
		super().__init__(
			pos, Vector3(0), mass=mass, size=size, color=color, 
			tail_color=tail_color
		)
		
		self.burn_time = burn_time
		self.burn_acc = burn_acc
		
		self.lifetime = 0.
		self.launch_time = launch_time
		self._gravity = False
		
		self._trajectory:np.ndarray|None = None
	
	def est_trajectory(self, n_pts:int=100):
		trajectory = []
		
		for t in np.linspace(0, self.burn_time+self.midcourse_time, num=n_pts):
			pos, _ = self.predict_pos_vel(self.bearing, t)
			trajectory.append(pos)
		
		return np.vstack(trajectory)
	
	def launch(self)->None:
		self.launch_time = self.lifetime
	
	@property
	def is_launched(self)->bool:
		return self.launch_time <= self.lifetime
	
	def create(self, sim:Simulation):
		super().create(sim)
	
	def predict_pos_vel(
		self, bearing:Vector3, t:Number
	)->Tuple[Vector3, Vector3]:
		'''
		Predicts the position and velocity t seconds after launch with the 
		given thrust bearing vector
		Assumes the missile has not been launched
		'''
		pos = self.pos.copy()
		vel = self.vel.copy()
		
		# Compute through the burn
		burn_time = min(self.burn_time, t)
		pos += vel*burn_time + 1/2*bearing*self.burn_acc*burn_time**2
		pos += 1/2*Vector3(0, 0, -G)*burn_time**2
		vel += self.burn_acc*bearing*burn_time + Vector3(0, 0, -G)*burn_time
		
		# If there is a midcourse phase, apply the existing velocity and
		# gravity
		if t > burn_time:
			midcourse_time = t-burn_time
			pos += vel*midcourse_time
			pos += 1/2*Vector3(0, 0, -G)*midcourse_time**2
			vel += Vector3(0, 0, -G)*midcourse_time
		
		return pos, vel
	
	def tick(self, delta_t:Number, time:Number)->None:
		super().tick(delta_t, time)
		
		self.lifetime += delta_t
		self._gravity = self.is_launched
		
		if self.launch_time <= self.lifetime \
			<= self.launch_time + self.burn_time:
			self.apply_accel(self.burn_acc*self.bearing)

	def draw(self, display:Renderer, time:Number)->None:
		super().draw(display, time)
		
		if self._trajectory is not None:
			display.axis.plot(
				*np.column_stack(self._trajectory),
				color=self.tail_color,
				linestyle='--',
				alpha=0.25
			)
