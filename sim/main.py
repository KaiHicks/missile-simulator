from sim.entities import Target
from sim.entities.missile.models import SimpleBalistic
from sim.simulation import Simulation
from sim.util.vector import Vector3


def main():
	target = Target(Vector3(1000, 1000, 0))
	bal_missile = SimpleBalistic(Vector3(0, 0, 1), target.pos, 3)
	
	simulation = Simulation([
		target, bal_missile
	])
	simulation.run()
	simulation.save('output.gif')

if __name__ == '__main__':
	main()
