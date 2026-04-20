import pygame
from drone import Drone
import math
import random

class Planet:
    cost = 0
    def __init__(self, position: tuple[int, int], color="#555555", drones=0, routes=[]):
        self.position = position
        self.size = 100
        self.color = color
        self.rect = pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)
        self.routes: list = routes

        self.max_visible_drones = 200
        self.tick_count = 0

        self.ticks_per_drone = 30
        self.ticks_per_orbit = 1000
        self.ticks_since_last_drone = 0
        self.angle_per_tick = (2*math.pi)/self.ticks_per_orbit
        self.orbit_distance = self.size*2
        self.drones_defending = 0 # purely visual dw about it too much

        self.visible_drones: list[Drone] = []
        self.number_of_drones = drones
        self.vulnerability = 1
        self.autosend = False

        self.add_visible_drones(drones)

    def add_visible_drones(self, amount=1):
        if amount <= 0:
            return
        for _ in range(amount):
            if len(self.visible_drones) >= self.max_visible_drones:
                break
            self.visible_drones.insert(0, Drone(self.position, self.color, random.random(), random.randint(0, self.ticks_per_orbit), self.size//20))

    def add_route(self, route):
        self.routes.append(route)

    def add_defending_drones(self, amount):
        self.drones_defending += amount * self.vulnerability

    def autosend_drones(self, route):
        self.autosend = route

    def stop_autosend(self):
        self.autosend = None

    def tick(self, amount):
        self.tick_count += amount

        if self.ticks_per_drone:
            self.ticks_since_last_drone += amount
            self.number_of_drones += self.ticks_since_last_drone // self.ticks_per_drone
            self.add_visible_drones(self.ticks_since_last_drone // self.ticks_per_drone)
            self.ticks_since_last_drone %= self.ticks_per_drone
            if self.autosend and self.number_of_drones > 0:
                self.send_drones(self.number_of_drones, self.autosend)

        for i, drone in enumerate(self.visible_drones):
            if i >= len(self.visible_drones)-self.drones_defending:
                drone.set_target(self.position)
            else:
                angle = self.angle_per_tick*(self.tick_count + drone.angle_offset) * 1/(drone.offset+0.5)
                drone.set_target((self.position[0]+(self.orbit_distance*(drone.offset/1.5+1))*math.cos(angle), self.position[1]+(self.orbit_distance*(drone.offset/1.5+1))*math.sin(angle)))

    def render_tick(self, timescale):
        for drone in self.visible_drones:
            drone.tick(timescale)

    def send_drones(self, amount, route):
        self.number_of_drones -= amount
        new_drones = [self.visible_drones.pop() for _ in range(min(len(self.visible_drones), amount))]
        route.get_drones(amount, new_drones, self)

    def get_drones(self, amount, visible_drones, drone_color):
        if drone_color == self.color: # adding drones
            self.number_of_drones += amount
            for drone in visible_drones:
                if len(self.visible_drones) < self.max_visible_drones:
                    drone.position = self.position
                    self.visible_drones.insert(0, drone)
        else: # getting attacked
            if self.number_of_drones <= amount*self.vulnerability: # if planet gets captured
                return Planet(self.position, drone_color, amount-(self.number_of_drones//self.vulnerability), self.routes)
            else:
                self.number_of_drones -= amount*self.vulnerability
                self.drones_defending -= amount*self.vulnerability
                self.visible_drones = self.visible_drones[:-(amount*self.vulnerability)]
                self.add_visible_drones(self.number_of_drones-len(self.visible_drones))
                return None
        # self.drones_defending = max(self.drones_defending-amount*self.vulnerability, 0)

    def get_render_info(self):
        if self.autosend and self.autosend.get_planets(self):
            planets = self.autosend.get_planets(self)
            autosend = (planets[1].position[0]-planets[0].position[0], planets[1].position[1]-planets[0].position[1])
            distance = math.dist(planets[1].position, planets[0].position)
            autosend = (autosend[0]/distance*self.size, autosend[1]/distance*self.size)
        else: autosend = None
        render_info = {
            "type": "normal",
            "position": self.position,
            "size": self.size,
            "color": self.color,
            "amount": self.number_of_drones,
            "drones": self.visible_drones,
            "autosend": autosend
        }
        return render_info

class UnclaimedPlanet(Planet):
    def __init__(self, position, color="#555555", drones=10, routes=[]):
        super().__init__(position, color, drones, routes)
        self.ticks_per_drone = None

    def get_drones(self, amount, visible_drones, drone_color):
        return super().get_drones(amount, visible_drones, drone_color)

class FactoryPlanet(Planet):
    cost = 25
    def __init__(self, position, color="#555555", drones=0, routes=[]):
        super().__init__(position, color, drones, routes)
        self.ticks_per_drone = self.ticks_per_drone//2
        self.vulnerability *= 2

    def get_render_info(self):
        render_info = super().get_render_info()
        render_info["type"] = "factory"
        return render_info

class TurretPlanet(Planet):
    cost = 10
    def __init__(self, position, color="#555555", drones=0, routes=[]):
        super().__init__(position, color, drones, routes)
        self.ticks_per_drone *= 2
        self.gun_ticks = 0

    def tick(self, amount):
        super().tick(amount)
        self.gun_ticks += amount
        minimum_distance = math.dist(self.routes[0].planet1.position, self.routes[0].planet2.position)

        for route in self.routes:
            pass

    def get_render_info(self):
        render_info = super().get_render_info()
        render_info["type"] = "turret"
        # autosend = (planets[1].position[0]-planets[0].position[0], planets[1].position[1]-planets[0].position[1])
        # distance = math.dist(planets[1].position, planets[0].position)
        # autosend = (autosend[0]/distance*self.size, autosend[1]/distance*self.size)
        return render_info