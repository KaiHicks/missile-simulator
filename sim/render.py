from numbers import Number
from typing import Callable

import matplotlib.pyplot as plt
from celluloid import Camera
from matplotlib.animation import ArtistAnimation


class Renderer:
	'''
	Manages the canvas and rendering
	'''
	size:int
	fps:float
	animation:ArtistAnimation|None
	
	_draw_fn:Callable[[], None]
	_last_refresh:float
	
	def __init__(self, draw_fn:Callable[[], None], size:int, fps:float=30):
		self.size = size
		self.fps = fps
		self.animation = None
		
		self._draw_fn = draw_fn
		self._last_refresh = -float('inf')
		
		self.fig, self.axis = plt.subplots(
			1,
			1,
			subplot_kw={'projection': '3d'},
			figsize=(self.size/50, self.size/50)
		)
		self.fig.tight_layout()
		
		self.axis.set_xlabel('x')
		self.axis.set_ylabel('y')
		self.axis.set_zlabel('z')
		
		self._camera = Camera(self.fig)
	
	def show(self):
		'''
		Renders and shows the animation
		'''
		self.animation = self._camera.animate(
			interval=1000/self.fps,
			blit=True
		)
		plt.show()
	
	def save(self, path:str='output.mp4'):
		'''
		Renders and saves the animation at the given path.
		'''
		self.animation = self._camera.animate(
			interval=1000/self.fps,
			blit=True
		)
		self.animation.save(path, fps=self.fps)
	
	def refresh(self, time:float)->None:
		'''
		Updates the canvas 
		'''
		if time >= self._last_refresh + 1/self.fps:
			self._draw_fn()
			self._camera.snap()
			self._last_refresh = time
