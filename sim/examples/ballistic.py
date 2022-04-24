'''
Shows a simulation of a number of ballistic missiles striking a target. 
'''

import numpy as np

from sim.entities import Target
from sim.entities.missile.models import SimpleBallistic
from sim.simulation import Simulation
from sim.util.vector import Vector3

N_MISSILES = 5

def main():
    # Create target and missiles
	target = Target(Vector3(1000, 1000, 0))
	bal_missiles = []
	for _ in range(N_MISSILES):
		# Want initial position normaly distributed around the origin
		initial_pos = Vector3(np.random.normal()*150, np.random.normal()*150, 1)
		bal_missiles.append(SimpleBallistic(initial_pos, target.pos, 3))
	
	# Create simulation object with the target and missiles
	simulation = Simulation([
		target, *bal_missiles
	])
	# Run and show it
	simulation.run()
	simulation.show()

if __name__ == '__main__':
	main()
