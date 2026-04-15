import pygame

class Planet:
    def __init__(self, position: tuple[int, int], size: int, ticks_per_drone=100):
        self.position = position
        self.size = size
        self.color = "#88DD88"
        self.rect = pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)
        self.routes: list = []
        self.drones = 0
        self.tick_count = 0
        self.ticks_per_drone = ticks_per_drone

    def add_route(self, route):
        self.routes.append(route)

    def tick(self):
        self.tick_count += 1
        if self.tick_count % self.ticks_per_drone == 0:
            self.drones += 1

    def send_drones(self, amount, route):
        self.drones -= amount
        route.get_drones(amount, self)

    def get_drones(self, amount):
        self.drones += amount

    def get_render_info(self):
        return {
            "position": self.position,
            "size": self.size,
            "color": self.color,
            "drones": self.drones
        }

