from numbers import Number
from sim.entities import Entity
from sim.util.vector import Vector3

class Explosion(Entity):
    def __init__(self, pos:Vector3, size:Number=10, color:str='red', time=0.1):
        self.pos = pos
        self.max_size = size
        self.color = color
        self.max_age = time

        self.age:Number = 0.
        self.alpha:Number = 1.
        self.size = 0.
    
    def tick(self, time_delta:Number, time:Number):
        self.alpha = 0.1**(self.age/self.max_age)
        self.size = self.max_size*self.age/self.max_age

        self.age += time_delta
        
        if self.age >= self.max_age:
            self.remove()