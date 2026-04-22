from planets import *
from route import Route

class GameAi:
    def __init__(self, map, planets=[], color="#DD8888"):
        self.color = color
        self.map = map
        self.tick_count = 0

    def send_if_able(self, origin: Planet, route: Route, other_planet: Planet):
        if not other_planet.ticks_per_drone:
            extra_drones = 0
        else:
            extra_drones = int(route.ticks_distance/other_planet.ticks_per_drone)
        defense_power = math.ceil((other_planet.number_of_drones+extra_drones)/other_planet.vulnerability)

        if origin.number_of_drones >= defense_power:
            origin.send_drones(defense_power, route)
            return True
        return False

    def try_upgrade_factory(self, planet: Planet):
        if not isinstance(planet, FactoryPlanet) and planet.number_of_drones >= FactoryPlanet.cost:
            self.map.upgrade_factory(planet)

    def try_upgrade_fort(self, planet: Planet):
        if not isinstance(planet, FortPlanet) and planet.number_of_drones >= FortPlanet.cost:
            self.map.upgrade_fort(planet)

    def recursive_autosend_drones(self, origin, safe_planets):
        for neighbor_route in origin.routes:
            neighbor_route: Route
            neighbor = neighbor_route.get_other_planet(origin)
            if not neighbor.autosend and neighbor in safe_planets and type(neighbor) != Planet: # specifically not including subclasses
                neighbor.autosend_drones(neighbor_route)
                self.recursive_autosend_drones(neighbor, safe_planets)

    def tick(self, amount):
        self.tick_count += amount
        if self.tick_count // 100 <= 0:
            return
        self.tick_count %= 100

        threatened_planets = []
        safe_planets = []

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
            enemy_planets: list[tuple[Route, Planet]] = []
            for route, neighbor in neighbors:
                if neighbor.color != self.color and not isinstance(neighbor, UnclaimedPlanet):
                    in_danger = True
                if isinstance(neighbor, UnclaimedPlanet):
                    unclaimed_planets.append((route, neighbor))
                elif neighbor.color != self.color:
                    enemy_planets.append((route, neighbor))

            for unclaimed_planet in unclaimed_planets:
                self.send_if_able(planet, unclaimed_planet[0], unclaimed_planet[1])

            if not in_danger:
                self.try_upgrade_factory(planet)
                safe_planets.append(planet)


            if in_danger:
                planet.stop_autosend()
                if len(enemy_planets) >= 2:
                    self.try_upgrade_fort(planet)
                danger_level = 0
                for enemy_planet in enemy_planets:
                    self.send_if_able(planet, enemy_planet[0], enemy_planet[1])
                    danger_level += enemy_planet[1].number_of_drones
                danger_level -= planet.number_of_drones//2
                danger_level * planet.vulnerability

                threatened_planets.append({
                    "planet": planet,
                    "enemy_drones": danger_level
                })

        if len(threatened_planets) > 0:
            threatened_planets.sort(key=lambda planet: planet["enemy_drones"])
            for threatened_planet_info in threatened_planets:
                threatened_planet = threatened_planet_info["planet"]
                self.recursive_autosend_drones(threatened_planet, safe_planets)