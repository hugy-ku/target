import pygame
from drone import Drone
import math
import random

class Planet:
    def __init__(self, position: tuple[int, int], size: int, color="#88DD88", ticks_per_drone=10, ticks_per_orbit=1000, orbit_distance=2, drones=0):
        self.position = position
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)
        self.routes: list = []
        self.drones: list[Drone] = []
        self.tick_count = 0
        self.ticks_per_drone = ticks_per_drone
        self.ticks_per_orbit = ticks_per_orbit
        self.angle_per_tick = (2*math.pi)/ticks_per_orbit
        self.orbit_distance = self.size*orbit_distance
        for _ in range(drones): self.add_drone()

    def add_drone(self):
        self.drones.append(Drone(self.position, self.color, random.random(), random.randint(0, self.ticks_per_orbit)))

    def add_route(self, route):
        self.routes.append(route)

    def tick(self):
        self.tick_count += 1
        if self.tick_count % self.ticks_per_drone == 0:
            self.add_drone()
        for drone in self.drones:
            angle = self.angle_per_tick*(self.tick_count + drone.angle_offset) * 1/(drone.offset+0.5)
            drone.set_target((self.position[0]+(self.orbit_distance*(drone.offset/1.5+1))*math.cos(angle), self.position[1]+(self.orbit_distance*(drone.offset/1.5+1))*math.sin(angle)))
            drone.tick()

    def send_drones(self, amount, route):
        new_drones = [self.drones.pop() for _ in range(amount)][::-1] # reversed to make sure that visible drones are both ordered last AND popped first
        route.get_drones(new_drones, self)

    def get_drones(self, drones):
        for drone in drones:
            drone.position = self.position
        self.drones = drones + self.drones

    def get_render_info(self):
        return {
            "position": self.position,
            "size": self.size,
            "color": self.color,
            "drones": self.drones
        }

