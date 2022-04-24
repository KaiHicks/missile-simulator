'''
Launches a number of ballistic missiles and then launches a number of 
interceptor ballistic missiles
'''

import numpy as np
from sim.entities.missile.models import BallisticInterceptor
from sim.entities.missile.models.simpleballistic import SimpleBallistic
from sim.entities.target import Target
from sim.simulation import Simulation
from sim.util.vector import Vector3


N_MISSILES = 3

def main():
	# Create target and strike missiles
	target = Target(Vector3(1000, 1000, 0))
	bal_missiles = []
	for _ in range(N_MISSILES):
		# Want initial position normaly distributed around the origin
		initial_pos = Vector3(
			np.random.normal()*150,
			np.random.normal()*150,
			1
		)
		bal_missiles.append(SimpleBallistic(initial_pos, target.pos, 3))
	
	# Create interceptor
	interceptors = []
	for bal in bal_missiles:
		initial_pos = Vector3(
			np.random.normal()*50,
			np.random.normal()*50,
			1
		)
		initial_pos += target.pos
		interceptors.append(BallisticInterceptor(initial_pos, bal, 2))
	
	# Create simulation object with the target and missiles
	simulation = Simulation([
		target, *bal_missiles, *interceptors
	])
	# Run and show it
	simulation.run()
	simulation.show()

if __name__ == '__main__':
	main()