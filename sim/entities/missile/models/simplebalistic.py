from enum import Enum, auto
from math import isnan
from numbers import Number

import numpy as np
from scipy import optimize
from scipy.optimize import fsolve

from sim.entities.missile import Missile
from sim.simulation import Simulation
from sim.util import G
from sim.util.vector import Vector3

class Phases(Enum):
	BOOST = auto()
	MIDCOURSE = auto()
	TERMINAL = auto()

class SimpleBalistic(Missile):
	'''
	A simple balistic missile which calculates its own launch bearing. The 
	missile has two phases, boost and midcourse. For the duration of the boost
	phase (controlled by burn_time), a constant acceleration of magnitude
	burn_acc is applied to the missile with the direction specified by bearing.
	The bearing is calculated using the initial position and the supplied
	target position. 
	'''
	
	target:Vector3
	burn_time:Number
	burn_acc:Number
	
	lifetime:float
	bearing:Vector3
	
	def __init__(
		self, pos:Vector3, target:Vector3, burn_time:Number, 
		burn_acc:Number=5*G, mass:Number=1, size:Number=None, color:str='blue',
		tail_color:str='teal'
	):
		super().__init__(
			pos, Vector3(0), mass=mass, size=size, color=color, 
			tail_color=tail_color
		)
		
		self.target = target
		self.burn_time = burn_time
		self.burn_acc = burn_acc
		
		self.lifetime = 0.
	
	def create(self, sim:Simulation):
		super().create(sim)

		self.bearing = self.compute_bearing()

	def est_displacement(self, thrust:Vector3, midcourse_time:float):
		'''
		Estimates the displacement after the thrust is vectored in the given 
		direction and the missile follows a balistic trajectory for 
		midcourse_time seconds. Estimation is performed using closed-form
		kinematic equations in constant time. 
		'''
		midcourse_time = abs(midcourse_time)
		
		boost_displacement = 1/2*self.burn_acc*thrust*self.burn_time**2
		boost_displacement += self.burn_acc*thrust \
			*self.burn_time*midcourse_time

		g_vec = np.array([0, 0, -G]).T
		g_displacement = 1/2*g_vec*self.burn_time**2
		g_displacement += 1/2*g_vec*midcourse_time**2
		g_displacement += g_vec*self.burn_time*midcourse_time

		return boost_displacement + g_displacement
	
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
			displacement = self.est_displacement(bearing, midcourse_time)
			
			return (self.pos + displacement - self.target).flatten()
		
		x = fsolve(
			cost,
			np.zeros((3,))
		)
		
		theta, phi, midcourse_time = x
		midcourse_time = abs(midcourse_time)

		bearing = to_bearing(theta, phi)
		
		print(bearing)
		print(f'Pitch: {90 - theta*180/np.pi:.4f}\u00B0')
		print(f'Midcourse time: {midcourse_time:,.4f}s')
		print(f'Flight time: {midcourse_time+self.burn_time:,.4f}s')

		print()
		print(f'Estimated displacement: {self.est_displacement(bearing, midcourse_time)}')
		print(f'{self.est_displacement(bearing, midcourse_time) - self.target}')
		print(f'Target: {self.target}')
		f_x = cost(x)
		print(f'Error: {(f_x.T @ f_x)**0.5:,.4f}m')
		
		return bearing
	
	def tick(self, delta_t:Number, time:Number)->None:
		super().tick(delta_t, time)
		
		self.lifetime += delta_t
		
		if self.lifetime <= self.burn_time:
			self.apply_accel(self.burn_acc*self.bearing)
