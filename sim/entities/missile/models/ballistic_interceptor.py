from numbers import Number
from typing import Tuple

import numpy as np
from scipy.optimize import fsolve
from sim.entities.missile.missile import Missile
from sim.entities.missile.models import Ballistic
from sim.simulation import Simulation
from sim.util import G
from sim.util.vector import Vector3


class BallisticInterceptor(Ballistic):
	def __init__(
		self, pos:Vector3, target:Ballistic, burn_time:Number, radius:Number=5,
		burn_acc:Number=5*G, mass:Number=1, size:Number=None, color:str='red', 
		tail_color:str='red'
	):
		super().__init__(
			pos, burn_time, burn_acc=burn_acc, 
			mass=mass, size=size, color=color, tail_color=tail_color
		)
		
		self.target = target
		self.radius = radius
		
		# Have we planned an interception path?
		self._target_lock = False
	
	def create(self, sim:Simulation):
		super().create(sim)
	
	def compute_bearing(self)->Tuple[Vector3, float]:
		'''
		Calculates the optimal thrust bearing for the boost phase to intercept
		the target
		'''
		def to_bearing(theta:float, phi:float)->Vector3:
			x = np.sin(phi)*np.cos(theta*2)
			y = np.sin(phi)*np.sin(theta*2)
			z = np.cos(phi)
			
			return Vector3(x, y, z)
		
		def cost(params:np.ndarray)->Vector3:
			theta, phi = params[:2]
			midcourse_time = abs(params[-1])
			
			bearing = to_bearing(theta, phi)
			pos, _ = self.predict_pos_vel(bearing, self.burn_time+midcourse_time)
			
			target_pos, _ = self.target.predict_pos_vel(
				self.target.bearing,
				self.burn_time+midcourse_time
			)
			
			return pos-target_pos
		
		x = fsolve(cost, np.zeros((3,)))
		
		theta, phi, midcourse_time = x
		midcourse_time = abs(midcourse_time)
		
		bearing = to_bearing(theta, phi)
		
		return bearing, midcourse_time
	
	def tick(self, delta_t:Number, time:Number)->None:
		super().tick(delta_t, time)
		
		can_launch = not self._target_lock \
			and hasattr(self.target, 'bearing')
		if can_launch:
			self.bearing, self.midcourse_time = self.compute_bearing()
			self._trajectory = self.est_trajectory()
			
			self._target_lock = True
			self.launch()
		
		if self.is_launched and not self.destroyed:
			residual = self.pos - self.target.pos
			if np.sqrt(residual.T@residual) <= self.radius:
				self.detonate()
				self.target.detonate()
		
