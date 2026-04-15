import pygame
from drone import Drone
import math
import random

class Planet:
    def __init__(self, position: tuple[int, int], size: int, ticks_per_drone=50, ticks_per_orbit=1000, orbit_distance=2):
        self.position = position
        self.size = size
        self.color = "#88DD88"
        self.rect = pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)
        self.routes: list = []
        self.drones: set[Drone] = set()
        self.tick_count = 0
        self.ticks_per_drone = ticks_per_drone
        self.ticks_per_orbit = ticks_per_orbit
        self.angle_per_tick = (2*math.pi)/ticks_per_orbit
        self.orbit_distance = self.size*orbit_distance

    def add_route(self, route):
        self.routes.append(route)

    def tick(self):
        self.tick_count += 1
        if self.tick_count % self.ticks_per_drone == 0:
            self.drones.add(Drone(self.position, self.color, random.uniform(0.75, 1.5), random.randint(0, self.ticks_per_orbit)))
        for drone in self.drones:
            angle = self.angle_per_tick*(self.tick_count + drone.angle_offset) * 1/drone.offset
            drone.set_position((self.position[0]+(self.orbit_distance*drone.offset)*math.cos(angle), self.position[1]+(self.orbit_distance*drone.offset)*math.sin(angle)))

    def send_drones(self, amount, route):
        new_drones = set(self.drones.pop() for _ in range(amount))
        route.get_drones(new_drones, self)

    def get_drones(self, amount):
        self.drones.update(amount)

    def get_render_info(self):
        return {
            "position": self.position,
            "size": self.size,
            "color": self.color,
            "drones": self.drones
        }

