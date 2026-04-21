from planets import *
from route import Route

class GameAi:
    def __init__(self, map, planets=[], color="#DD8888"):
        self.color = color
        self.map = map

    def send_if_able(self, origin: Planet, route: Route, other_planet: Planet):
        if not other_planet.ticks_per_drone:
            extra_drones = 0
        else:
            extra_drones = route.ticks_distance*other_planet.ticks_per_drone

        if origin.number_of_drones >= other_planet.number_of_drones+extra_drones:
            origin.send_drones(other_planet.number_of_drones+extra_drones, route)
            return True
        return False

    def try_upgrade_factory(self, planet: Planet):
        if not isinstance(planet, FactoryPlanet) and planet.number_of_drones >= FactoryPlanet.cost:
            self.map.upgrade_factory(planet)

    def try_upgrade_fort(self, planet: Planet):
        if not isinstance(planet, FortPlanet) and planet.number_of_drones >= FortPlanet.cost:
            self.map.upgrade_fort(planet)

    def tick(self):
        for planet in self.map.planets:
            if planet.color != self.color:
                continue

            neighbors: list[tuple[Route, Planet]] = []
            for route in planet.routes:
                route: Route
                neighbor = route.get_other_planet(planet)
                if neighbor:
                    neighbors.append((route, neighbor))

            in_danger = False
            unclaimed_planets: list[tuple[Route, Planet]] = []
            for route, neighbor in neighbors:
                if neighbor.color != self.color and not isinstance(neighbor, UnclaimedPlanet):
                    in_danger = True
                if isinstance(neighbor, UnclaimedPlanet):
                    unclaimed_planets.append((route, neighbor))

            for unclaimed_planet in unclaimed_planets:
                self.send_if_able(planet, unclaimed_planet[0], unclaimed_planet[1])

            if not in_danger:
                self.try_upgrade_factory(planet)

            if in_danger:
                self.try_upgrade_fort(planet)