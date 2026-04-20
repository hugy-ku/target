import pygame
import math
from planets import Planet
from drone import Drone

class Route:
    def __init__(self, planet1: Planet, planet2: Planet, size):
        self.planet1 = planet1
        self.planet2 = planet2
        self.size = size
        self.drones = []
        # heavenly code
        x1 = min(self.planet1.position[0]-self.planet1.size, self.planet2.position[0]-self.planet2.size)
        y1 = min(self.planet1.position[1]-self.planet1.size, self.planet2.position[1]-self.planet2.size)
        x2 = max(self.planet1.position[0]+self.planet1.size, self.planet2.position[0]+self.planet2.size)
        y2 = max(self.planet1.position[1]+self.planet1.size, self.planet2.position[1]+self.planet2.size)
        self.rect = pygame.Rect(x1, y1, x2-x1, y2-y1)
        self.ticks_distance = int(math.dist((x1, y1), (x2, y2))/5)
        self.distance_per_tick = (
            (planet2.position[0]-planet1.position[0])/self.ticks_distance,
            (planet2.position[1]-planet1.position[1])/self.ticks_distance
        )

    def get_planets(self, origin):
        if origin == self.planet1:
            return self.planet1, self.planet2
        if origin == self.planet2:
            return self.planet2, self.planet1

    def get_drones(self, amount, visible_drones: list[Drone], origin_planet: Planet):
        if origin_planet == self.planet1:
            # print(f"route {self.planet1.position} to {self.planet2.position}")
            self.drones.append({
                "ticks": 0,
                "amount": amount,
                "visible_drones": visible_drones,
                "color": origin_planet.color,
                "reverse": False,
                "position": self.get_pos_from_tick(0),
                "attacking": False
            })
        else:
            # print(f"route {self.planet2.position} to {self.planet1.position}")
            self.drones.append({
                "ticks": self.ticks_distance,
                "amount": amount,
                "visible_drones": visible_drones,
                "color": origin_planet.color,
                "reverse": True,
                "position": self.get_pos_from_tick(self.ticks_distance),
                "attacking": False
            })

    def tick(self, amount):
        for drones in self.drones:

            if not drones["reverse"]:
                drones["ticks"] += amount
                if not drones["attacking"] and drones["color"] != self.planet2.color and drones["ticks"] >= self.ticks_distance-self.planet2.size:
                    self.planet2.add_defending_drones(len(drones["visible_drones"]))
                    drones["attacking"] = True
                if drones["ticks"] >= self.ticks_distance:
                    self.drones.remove(drones)
                    self.planet2.get_drones(drones["amount"], drones["visible_drones"], drones["color"])
                drones["position"] = self.get_pos_from_tick(drones["ticks"])
            else:
                drones["ticks"] -= amount
                if not drones["attacking"] and drones["color"] != self.planet1.color and drones["ticks"] <= self.planet1.size:
                    self.planet1.add_defending_drones(len(drones["visible_drones"]))
                    drones["attacking"] = True
                if drones["ticks"] <= 0:
                    self.drones.remove(drones)
                    self.planet1.get_drones(drones["amount"], drones["visible_drones"], drones["color"])
                drones["position"] = self.get_pos_from_tick(drones["ticks"])

            for other_drones in self.drones:
                if drones == other_drones:
                    continue
                # print(f"comparing {drones["ticks"]} with {other_drones["ticks"]}")
                if drones["color"] != other_drones["color"] and drones["ticks"] >= other_drones["ticks"]-amount and drones["ticks"] <= other_drones["ticks"]+amount:
                    temp = drones["amount"]
                    drones["amount"] -= other_drones["amount"]
                    other_drones["amount"] -= temp
                    drones["visible_drones"] = drones["visible_drones"][:min(drones["amount"], len(drones["visible_drones"]))]
                    other_drones["visible_drones"] = other_drones["visible_drones"][:min(other_drones["amount"], len(other_drones["visible_drones"]))]
                    if drones["amount"] <= 0:
                        self.drones.remove(drones)
                        break
                    if other_drones["amount"] <= 0: self.drones.remove(other_drones)

            for drone in drones["visible_drones"]:
                drone.set_target((
                    drones["position"][0] + 100*((drone.offset)*math.cos(drone.angle_offset)),
                    drones["position"][1] + 100*((drone.offset)*math.sin(drone.angle_offset))
                ))

    def render_tick(self, timescale):
        for drones in self.drones:
            for drone in drones["visible_drones"]:
                drone.tick(timescale)

    def get_pos_from_tick(self, tick):
        return (self.planet1.position[0]+self.distance_per_tick[0]*tick, self.planet1.position[1]+self.distance_per_tick[1]*tick)

    def get_render_info(self):
        return {
            "position1": self.planet1.position,
            "position2": self.planet2.position,
            "size": self.size,
            "color": "#BBBBBB",
            "drones": self.drones
        }