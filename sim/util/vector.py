from ast import Num
from numbers import Number
import numpy as np

class Vector3(np.ndarray):
	def __new__(
		self, x:Number, y:Number=None, z:Number=None, dtype=np.float64
	):
		if y is None:
			y = float(x)
		if z is None:
			z = float(x)
		
		self = np.asarray([x, y, z], dtype=dtype).view(Vector3)
		return self
	
	@property
	def x(self):
		return self[0]
	@x.setter
	def x(self, new_x):
		self[0] = new_x
	@property
	def y(self):
		return self[1]
	@y.setter
	def y(self, new_y):
		self[1] = new_y
	@property
	def z(self):
		return self[2]
	@z.setter
	def z(self, new_z):
		self[2] = new_z
	
	def __str__(self):
		return f'({self.x:,.2f}, {self.y:,.2f}, {self.z:,.2f})'
	
	def __repr__(self):
		return f'{self.__class__}({self.x}, {self.y}, {self.z})'