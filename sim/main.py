from mimetypes import init
import numpy as np

from sim.entities import Target
from sim.entities.missile.models import SimpleBalistic
from sim.simulation import Simulation
from sim.util.vector import Vector3

N_MISSILES = 5

def main():
	target = Target(Vector3(1000, 1000, 0))
	bal_missiles = []
	for _ in range(N_MISSILES):
		initial_pos = Vector3(np.random.normal()*150, np.random.normal()*150, 1)
		bal_missiles.append(SimpleBalistic(initial_pos, target.pos, 3))
	
	simulation = Simulation([
		target, *bal_missiles
	])
	simulation.run()
	simulation.save('output.gif')

if __name__ == '__main__':
	main()
