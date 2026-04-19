import pygame
from planets import Planet
from route import Route
import random
import math
import multiprocessing

class Map:
    def __init__(self):
        self.map_rect = None
        self.planets: list[Planet] = []
        self.routes: list[Route] = []
        self.active = None
        self.hover = None

    def add_planet(self, position, size=100):
        planet = Planet(position, size)
        self.planets.append(planet)
        return planet

    def add_route(self, planet1: Planet, planet2: Planet, size=100):
        route = Route(planet1, planet2, size)
        planet1.add_route(route)
        planet2.add_route(route)
        self.routes.append(route)

    def get_route(self, planet1: Planet, planet2: Planet):
        for route in planet1.routes:
            if route.planet1 == planet1 and route.planet2 == planet2 or route.planet1 == planet2 and route.planet2 == planet1:
                return route
        return None

    def check_hover(self, map_mouse_pos):
        for planet in self.planets:
            if planet.rect.collidepoint(map_mouse_pos):
                self.hover = planet
                return
        self.hover = None

    def check_active(self):
        if self.hover and self.active != self.hover:
            self.select_planet(self.active, self.hover)
        else:
            self.active = None

    def select_planet(self, sender, receiver):
        if not self.active:
            self.active = self.hover
            return
        # print(f"sender: {sender.position}, receiver: {receiver.position}")
        route = self.get_route(sender, receiver)
        if not route:
            self.active = None
            return

        self.active.send_drones(self.active.number_of_drones, route)
        self.active = None

    def random_generate(self, map_size, target_number_of_planets=10):
        self.map_rect = pygame.Rect(0, 0, map_size[0], map_size[1])
        distance_threshold = 500
        for _ in range(target_number_of_planets):
            position = (random.randint(0, map_size[0]), random.randint(0, map_size[1]))
            distance_sorted = self.planets.copy()
            distance_sorted.sort(key=lambda planet: math.dist(planet.position, position))
            if len(distance_sorted) > 0 and math.dist(distance_sorted[0].position, position) < distance_threshold:
                continue
            planet = Planet(position, drones=10, ticks_per_drone=None)
            self.planets.append(planet)

            for i, other_planet in enumerate(distance_sorted):
                if i == 0:
                    self.add_route(planet, other_planet)

        # test
        self.planets[0].color = "#DD8888"
        self.planets[0].visible_drones = []
        self.planets[0].number_of_drones = 0
        self.planets[0].ticks_per_drone = 10

        self.planets[-1].color = "#88DD88"
        self.planets[-1].visible_drones = []
        self.planets[-1].number_of_drones = 0
        self.planets[-1].ticks_per_drone = 10


    def tick(self, amount):
        for planet in self.planets:
            planet.tick(amount)
        for route in self.routes:
            route.tick(amount)

    def render_tick(self, timescale):
        for planet in self.planets:
            planet.render_tick(timescale)
        for route in self.routes:
            route.render_tick(timescale)

    def get_render_info(self):
        planets = []
        routes = []
        for planet in self.planets:
            planets.append(planet.get_render_info())
        for route in self.routes:
            routes.append(route.get_render_info())

        if self.hover:
            hover_info = self.hover.get_render_info()
        else:
            hover_info = None
        if self.active:
            active_info = self.active.get_render_info()
        else:
            active_info = None

        return {
            "planets": planets,
            "routes": routes,
            "hover": hover_info,
            "active": active_info
        }