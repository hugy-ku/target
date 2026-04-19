import pygame
from drone import Drone
import math
import random

class Planet:
    def __init__(self, position: tuple[int, int], size: int, color="#88DD88", ticks_per_drone=10, ticks_per_orbit=1000, orbit_distance=2, drones=0, max_visible_drones=200):
        self.position = position
        self.size = size
        self.color = color
        self.rect = pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)
        self.routes: list = []
        self.max_visible_drones = max_visible_drones
        self.tick_count = 0

        self.ticks_per_drone = ticks_per_drone
        self.ticks_per_orbit = ticks_per_orbit
        self.ticks_since_last_drone = 0
        self.angle_per_tick = (2*math.pi)/ticks_per_orbit
        self.orbit_distance = self.size*orbit_distance
        self.drones_defending = 0 # purely visual dw about it too much

        self.visible_drones: list[Drone] = []
        self.number_of_drones = drones
        self.vulnerability = 1

        self.add_visible_drones(drones)

    def add_visible_drones(self, amount=1):
        if amount <= 0:
            return
        for _ in range(amount):
            self.visible_drones.insert(0, Drone(self.position, self.color, random.random(), random.randint(0, self.ticks_per_orbit), self.size//20))
        self.visible_drones = self.visible_drones[:self.max_visible_drones]

    def add_route(self, route):
        self.routes.append(route)

    def set_defending_drones(self, amount):
        self.drones_defending = amount * self.vulnerability

    def tick(self, amount):
        self.tick_count += amount
        self.ticks_since_last_drone += amount

        self.number_of_drones += self.ticks_since_last_drone // self.ticks_per_drone
        self.add_visible_drones(self.ticks_since_last_drone // self.ticks_per_drone)
        self.ticks_since_last_drone %= self.ticks_per_drone

        for i, drone in enumerate(self.visible_drones):
            angle = self.angle_per_tick*(self.tick_count + drone.angle_offset) * 1/(drone.offset+0.5)
            if i >= len(self.visible_drones)-self.drones_defending:
                drone.set_target(self.position)
            else:
                drone.set_target((self.position[0]+(self.orbit_distance*(drone.offset/1.5+1))*math.cos(angle), self.position[1]+(self.orbit_distance*(drone.offset/1.5+1))*math.sin(angle)))

    def render_tick(self, timescale):
        for drone in self.visible_drones:
            drone.tick(timescale)

    def send_drones(self, amount, route):
        self.number_of_drones -= amount
        new_drones = [self.visible_drones.pop() for _ in range(min(len(self.visible_drones), amount))]
        route.get_drones(amount, new_drones, self)

    def get_drones(self, amount, visible_drones, drone_color):
        if drone_color == self.color:
            self.number_of_drones += amount
            for drone in visible_drones:
                if len(self.visible_drones) < self.max_visible_drones:
                    drone.position = self.position
                    self.visible_drones.insert(0, drone)
        else:
            if self.number_of_drones <= amount*self.vulnerability:
                self.color = drone_color
                self.number_of_drones = amount - (self.number_of_drones//self.vulnerability)
                self.visible_drones = []
                self.add_visible_drones(self.number_of_drones)
            else:
                self.number_of_drones -= amount*self.vulnerability
                self.visible_drones = self.visible_drones[:-self.drones_defending]
                self.add_visible_drones(min(self.number_of_drones-len(self.visible_drones), self.max_visible_drones-len(self.visible_drones)))
        self.drones_defending = 0

    def get_render_info(self):
        return {
            "position": self.position,
            "size": self.size,
            "color": self.color,
            "amount": self.number_of_drones,
            "drones": self.visible_drones
        }

