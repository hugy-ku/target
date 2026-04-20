import pygame
from planets import *
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
        self.dragging = False
        self.first_drag = False
        self.distance_threshold = 500
        self.alert = ""
        self.alert_timer = 0

    def set_alert(self, alert):
        self.alert = alert
        self.alert_timer = 2000

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

    def get_active(self):
        return self.active

    def check_hover(self, map_mouse_pos):
        for planet in self.planets:
            if planet.rect.collidepoint(map_mouse_pos):
                self.hover = planet
                return
        self.hover = None

    def mousedown(self):
        if self.hover and self.hover == self.active:
            self.dragging = self.active
            self.first_drag = False
        if self.hover and not self.active:
            self.active = self.hover
            self.dragging = self.active
            self.first_drag = True

        if self.hover and self.active and self.active != self.hover:
            self.send_drones(self.active, self.hover)
            self.active = None
        if not self.hover:
            self.active = None

    def mouseup(self):
        if not self.hover or self.hover and self.hover == self.active:
            self.dragging = None
            if not self.first_drag and self.active:
                self.stop_autosend(self.active)
                self.active = None
            return
        if self.active and self.active != self.hover:
            self.autosend_drones(self.active, self.hover)
            self.active = None
            self.dragging = None

    def autosend_drones(self, sender: Planet, receiver: Planet):
        route = self.get_route(sender, receiver)
        self.active.autosend_drones(route)

    def stop_autosend(self, planet: Planet):
        planet.stop_autosend()

    def send_drones(self, sender: Planet, receiver: Planet):
        # print(f"sender: {sender.position}, receiver: {receiver.position}")
        route = self.get_route(sender, receiver)
        if not route:
            return
        sender.send_drones(sender.number_of_drones, route)

    def replace_planet(self, origin, replacing):
        for new_route in origin.routes:
            new_route.replace_planet(origin, replacing)
        self.planets[self.planets.index(origin)] = replacing

    def upgrade_factory(self):
        if not self.active:
            return
        if isinstance(self.active, FactoryPlanet):
            self.active = None
            self.set_alert("Planet is already a factory")
            return
        if self.active.number_of_drones < FactoryPlanet.cost:
            self.set_alert(f"You need {FactoryPlanet.cost} drones to upgrade")
            return
        self.replace_planet(self.active, FactoryPlanet(self.active.position, self.active.color, self.active.number_of_drones-FactoryPlanet.cost, self.active.routes))
        self.active = None

    def shuffle_planet(self, planet: Planet):
        planet_position = planet.position
        distance_sorted = self.planets
        distance_sorted.sort(key=lambda other_planet: math.dist(other_planet.position, planet_position))
        if math.dist(distance_sorted[0].position, planet_position) < self.distance_threshold:
            nearest_planet = distance_sorted[0]
            planet_position = (planet_position[0]-(nearest_planet.position[0]-planet_position[0])*random.random(), planet_position[1]-(nearest_planet.position[1]-planet_position[1])*random.random())
        planet.position = planet_position

    def random_generate(self, map_size, target_number_of_planets=10):
        self.map_rect = pygame.Rect(0, 0, map_size[0], map_size[1])
        for _ in range(target_number_of_planets):
            position = (random.randint(0, map_size[0]), random.randint(0, map_size[1]))
            distance_sorted = self.planets.copy()

            if len(distance_sorted) <= 0:
                planet = UnclaimedPlanet(position)
                self.planets.append(planet)
                continue

            distance_sorted.sort(key=lambda planet: math.dist(planet.position, position))
            if math.dist(distance_sorted[0].position, position) < self.distance_threshold/2:
                continue
            planet = UnclaimedPlanet(position)
            self.planets.append(planet)

        for planet in self.planets:
            for _ in range(5):
                self.shuffle_planet(planet)

        for i, planet in enumerate(self.planets):
            other_planets = self.planets[i+1:]
            if len(other_planets) <= 0:
                continue
            other_planets.sort(key=lambda other_planet: math.dist(planet.position, other_planet.position))
            for other_planet in other_planets:
                if math.dist(planet.position, other_planet.position) < self.distance_threshold*1.5:
                    self.add_route(planet, other_planet)
            if not self.get_route(planet, other_planets[0]):
                self.add_route(planet, other_planets[0])

        # test
        self.replace_planet(self.planets[0], Planet(self.planets[0].position, "#DD8888", routes=self.planets[0].routes))
        self.replace_planet(self.planets[-1], Planet(self.planets[-1].position, "#88DD88", routes=self.planets[0].routes))

    def tick(self, amount):

        for planet in self.planets:
            planet.tick(amount)
        for route in self.routes:
            new_planets = route.tick(amount)
            if new_planets:
                self.replace_planet(new_planets[0], new_planets[1])

    def render_tick(self, timescale):
        if self.alert_timer > 0:
            self.alert_timer -= timescale
            if self.alert_timer <= 0:
                self.alert = None

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