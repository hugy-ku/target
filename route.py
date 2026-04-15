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
        self.ticks_distance = math.dist((x1, y1), (x2, y2))/5
        self.distance_per_tick = ((planet2.position[0]-planet1.position[0])/self.ticks_distance, (planet2.position[1]-planet1.position[1])/self.ticks_distance)

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
        for drones in self.drones:
            if not drones["reverse"]:
                drones["ticks"] += 1
                if drones["ticks"] >= self.ticks_distance:
                    self.drones.remove(drones)
                    self.planet2.get_drones(drones["amount"])

            else:
                drones["ticks"] -= 1
                if drones["ticks"] <= 0:
                    self.drones.remove(drones)
                    self.planet1.get_drones(drones["amount"])

            for drone in drones["amount"]:
                drone.set_target((
                    self.planet1.position[0]+self.distance_per_tick[0]*drones["ticks"] + 100*((drone.offset)*math.cos(drone.angle_offset)),
                    self.planet1.position[1]+self.distance_per_tick[1]*drones["ticks"] + 100*((drone.offset)*math.sin(drone.angle_offset))
                ))
                drone.tick()


    def get_render_info(self):
        return {
            "position1": self.planet1.position,
            "position2": self.planet2.position,
            "size": self.size,
            "color": "#BBBBBB",
            "drones": self.drones
        }