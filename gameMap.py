import pygame
from planets import *
from route import Route
from gameAi import GameAi
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
        self.ai_colors = ["#DD8888"]
        self.ais: list[GameAi] = []

    def set_alert(self, alert):
        self.alert = alert
        self.alert_timer = 2000

    def add_planet(self, position, size=100):
        planet = Planet(position, size)
        self.planets.append(planet)
        return planet

    def add_route(self, planet1: Planet, planet2: Planet):
        route = Route(planet1, planet2)
        planet1.add_route(route)
        planet2.add_route(route) # me desperately trying and failing to turn a directed graph into and undirected graph
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

    def mousedown(self, button):
        if button == 1:
            if self.hover and self.active and self.hover == self.active:
                self.dragging = self.active
                self.first_drag = False
            if self.hover and not self.active and self.hover.color == "#88DD88":
                self.active = self.hover
                self.dragging = self.active
                self.first_drag = True

        if self.hover and self.active and self.active != self.hover:
            if button == 1:
                self.send_drones(self.active, self.hover, 1)
                self.active = None
            elif button == 3:
                self.send_drones(self.active, self.hover,0.5)
                # not adding self.active = None here since sending half implies that you want to continue sending more
        if not self.hover:
            self.active = None

    def mouseup(self, button):
        if button != 1:
            return
        if not self.hover or self.hover and self.active and self.hover == self.active:
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

    def send_drones(self, sender: Planet, receiver: Planet, amount):
        # print(f"sender: {sender.position}, receiver: {receiver.position}")
        route = self.get_route(sender, receiver)
        if not route:
            return
        sender.send_drones(math.ceil(sender.number_of_drones*amount), route)

    def replace_planet(self, origin, replacing):
        for new_route in origin.routes:
            new_route.replace_planet(origin, replacing)
        try:
            self.planets[self.planets.index(origin)] = replacing
        except ValueError:
            pass

    def upgrade_factory(self, planet: Planet):
        self.replace_planet(planet, FactoryPlanet(planet.position, planet.color, planet.number_of_drones-FactoryPlanet.cost, planet.routes))

    def user_upgrade_factory(self):
        if not self.active:
            return
        if isinstance(self.active, FactoryPlanet):
            self.active = None
            self.set_alert("Planet is already a factory")
            return
        if self.active.number_of_drones < FactoryPlanet.cost:
            self.set_alert(f"You need {FactoryPlanet.cost} drones to upgrade")
            return
        self.upgrade_factory(self.active)
        self.active = None

    def upgrade_fort(self, planet: Planet):
        self.replace_planet(planet, FortPlanet(planet.position, planet.color, planet.number_of_drones-FortPlanet.cost, planet.routes))

    def user_upgrade_fort(self):
        if not self.active:
            return
        if isinstance(self.active, FortPlanet):
            self.active = None
            self.set_alert("Planet is already a turret")
            return
        if self.active.number_of_drones < FortPlanet.cost:
            self.set_alert(f"You need {FortPlanet.cost} drones to upgrade")
            return
        self.upgrade_fort(self.active)
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
            if Route(planet, other_planets[0]) not in self.routes:
                self.add_route(planet, other_planets[0])

    def new_map(self, map_size, target_number_of_planets=10):
        self.__init__()
        self.random_generate(map_size, target_number_of_planets)
        self.replace_planet(self.planets[-1], Planet(self.planets[-1].position, "#88DD88", routes=self.planets[-1].routes))
        for color in self.ai_colors:
            new_planet = Planet(self.planets[0].position, color, routes=self.planets[0].routes)
            self.replace_planet(self.planets[0], new_planet)
            self.ais.append(GameAi(self, [new_planet], color))

    def tick(self, amount):
        for planet in self.planets:
            planet.tick(amount)
        for route in self.routes:
            new_planets = route.tick(amount)
            if new_planets:
                self.replace_planet(new_planets[0], new_planets[1])
        for ai in self.ais:
            ai.tick(amount)

    def check_win(self):
        colors = set()
        for planet in self.planets:
            if isinstance(planet, UnclaimedPlanet):
                continue
            colors.add(planet.color)
        for route in self.routes:
            for drones in route.drones:
                colors.add(drones["color"])
        return colors.pop() if len(colors) <= 1 else None

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