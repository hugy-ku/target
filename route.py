import pygame
import math
from planets import Planet

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
        self.ticks_distance = math.dist((x1, y1), (x2, y2))/3

    def get_drones(self, amount, origin_planet):
        if origin_planet == self.planet1:
            self.drones.append({
                "ticks": 0,
                "amount": amount,
                "reverse": False
            })
        else:
            self.drones.append({
                "ticks": self.ticks_distance,
                "amount": amount,
                "reverse": True
            })

    def tick(self):
        for drone in self.drones:
            if not drone["reverse"]:
                drone["ticks"] += 1
                if drone["ticks"] >= self.ticks_distance:
                    self.drones.remove(drone)
                    self.planet2.get_drones(drone["amount"])
            else:
                drone["ticks"] -= 1
                if drone["ticks"] <= 0:
                    self.drones.remove(drone)
                    self.planet1.get_drones(drone["amount"])

    def get_render_info(self):
        return {
            "position1": self.planet1.position,
            "position2": self.planet2.position,
            "size": self.size,
            "color": "#BBBBBB"
        }