from enum import Enum, auto
from numbers import Number

import numpy as np
from scipy.optimize import fsolve

from sim.entities.missile.models import Ballistic
from sim.render import Renderer
from sim.simulation import Simulation
from sim.util import G
from sim.util.vector import Vector3

class Phases(Enum):
	BOOST = auto()
	MIDCOURSE = auto()
	TERMINAL = auto()

class SimpleBallistic(Ballistic):
	'''
	A simple ballistic missile which calculates its own launch bearing. The 
	missile has two phases, boost and midcourse. For the duration of the boost
	phase (controlled by burn_time), a constant acceleration of magnitude
	burn_acc is applied to the missile with the direction specified by bearing.
	The bearing is calculated using the initial position and the supplied
	target position. 
	'''
	def __init__(
		self, pos:Vector3, target:Vector3, burn_time:Number, 
		launch_time:Number=0, burn_acc:Number=5*G, mass:Number=1, 
		size:Number=None, color:str='blue', tail_color:str='teal'
	):
		super().__init__(
			pos, burn_time, launch_time=launch_time, burn_acc=burn_acc, 
			mass=mass, size=size, color=color, tail_color=tail_color
		)
		
		self.target = target
	
	def create(self, sim:Simulation):
		super().create(sim)

		self.bearing, self.midcourse_time = self.compute_bearing()
		self._trajectory = self.est_trajectory()

	def est_trajectory(self, n_pts=100):
		trajectory = []
		pts_per_s = n_pts/(self.burn_time + self.midcourse_time)
		
		for t in np.linspace(
			0,
			self.burn_time,
			num=int(pts_per_s*self.burn_time)
		):
			pos, _ = self.predict_pos_vel(self.bearing, t)
			trajectory.append(pos)
		for t in np.linspace(
			self.burn_time,
			self.burn_time + self.midcourse_time,
			num=int(pts_per_s*self.midcourse_time)
		):
			pos, _ = self.predict_pos_vel(self.bearing, t)
			trajectory.append(pos)
		
		trajectory = np.vstack(trajectory)
		return trajectory

	def compute_bearing(self):
		'''
		Calculates the optimal bearing for the thrust in the boost phase to
		hit the target. 
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
			final_pos, _ = self.predict_pos_vel(
				bearing,
				self.burn_time+midcourse_time
			)
			
			return (final_pos - self.target).flatten()
		
		x = fsolve(
			cost,
			np.zeros((3,))
		)
		
		theta, phi, midcourse_time = x
		midcourse_time = abs(midcourse_time)

		bearing = to_bearing(theta, phi)
		
		return bearing, midcourse_time
	
	def draw(self, display:Renderer, time:Number)->None:
		super().draw(display, time)
		display.axis.plot(
			*np.column_stack(self._trajectory),
			color=self.tail_color,
			linestyle='--',
			alpha=0.25
		)
