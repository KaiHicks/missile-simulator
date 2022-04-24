# Missile Defense Simulator

<p align="center">
	<img src="https://github.com/KaiHicks/missile-simulator/blob/master/readme_animation.gif?raw=true" width=50%>
	<center>Figure 1: A ballistic interceptor simulation</center>
</p>

This program is a playground for simple missile defense simulations. Currently, ballistic missiles and ballistic interceptors have been implemented. 

## Setup
You can install dependancies either with pipenv (preferred) or with venv. Requires python 3.10.x or greater. 

### Pipenv

First, install dependencies with
```python3 -m pipenv install```
Next, enter the virtual environment
```python3 -m pipenv shell```

### Venv/pip

Create a virtual environment
```python3 -m venv env```
Enter the virtual environment (may be different if not using bash)
```source env/bin/activate```
Then, install dependencies
```python3 -m pip install -r requirements.txt```

## Using the Simulator

To run the simulator, do
```python3 -m sim.main```

A basic simulation includes a missile and a target. First import all necessary components
```
from sim.entities import Target
from sim.entities.missile.models import SimpleBallistic
from sim.simulation import Simulation
from sim.util.vector import Vector3
```
Then, create a target. Here, `Vector3(1000, 1000, 0)` is the target's position. This is an entity that is used to draw the target location on the screen.
```
target = Target(Vector3(1000, 1000, 0))
```
Next, create a ballistic missile with a burn time of three seconds, the initial position set to `Vector3(0, 0, 1)`, and the target entity's position as its target.
```
bal_missile = SimpleBallistic(Vector3(0, 0, 1), target.pos, 3)
```
After creating all the entities, we can now create and run the simulation.
```
simulation = Simulation([
	target, bal_missile
])
simulation.run()
```
After some processing, the simulation has run, but nothing has been displayed or output. The simulation frames have been saved in memory and still need to be rendered. This is accomplished by calling `simulation.show()` or `simulation.save(path)`. The `show()` call will render and display the simulation in a GUI that supports repositioning the camera. The `save(path)` call simply renders the simulation and saves the video to the provided file path. 
```
simulation.save('output.gif')
```
Saving the simulation can take a long time and may require you to install `ffmpeg` and/or `H.264` through your system's package manager. For this reason, it is always a good idea to prototype/debug using `show()` calls, and then saving once everything is working. Alternatively, if you meerly wish to watch the simulation, you can instead call 
```
simulation.show()
```

## Technical Details

### Kinematics Engine

The kinematics engine is tasked with predicting the positions and velocities of each object given their accelerations over time. This is achieved using [leapfrog integration](https://en.wikipedia.org/wiki/Leapfrog_integration). Leapfrog integration discretizes the time domain into a series of ticks. Every tick, the new position of each object is computed using classical mechanics, assuming a constant acceleration. Currently, the simulator assume air resistance is negligible, but I have plans to add drag in the future. 

### Ballistic Missile

A ballistic missile (modeled in `Ballistic`) applies a constant acceleration over a fixed duration at a set direction. After which, the missile follows a ballistic trajectory, hence the name. Note that a real ballistic missile violates every one of these assumptions to some degree. To aim the missile, one must adjust the direction of thrust. In this project, this is done by modeling the trajectory with classical mechanics. Then, a numerical solver is used to compute the thrust direction. 

### Ballistic Interception

The `BallisticInterceptor` object is a ballistic missile that targets another ballistic missile, instead of a static target. Computing the thrust direction for the ballistic interceptor is, while technically more complicated, very similar to the regular ballistic missile. Instead of simply modeling the trajectory of the interceptor, we must model the interceptor and the target. Then, we again use a numerical solver to optimize the difference between the interceptor and target positions. 