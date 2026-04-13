import pygame
import time

class MainGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200), pygame.RESIZABLE)
        self.clock = pygame.Clock()
        self.running = True
        self.delta_time = 0
        self.map = Map()
        self.map.generate_map((500, 500))
        self.renderManager = RenderManager(self.map)

        self.mouse_pos = None

        self.mainloop()

    def mainloop(self):
        while self.running:
            self.mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                print(event) # debug
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)
            self.handle_hold_inputs()
            self.renderManager.render(self.map, self.screen)
            pygame.display.flip()

            self.delta_time = self.clock.tick(60)

    def handle_input(self, event: pygame.event.Event):

        if event.type == pygame.MOUSEWHEEL:
            self.renderManager.change_zoom(event.y*0.05, self.mouse_pos, self.screen.size)


    def handle_hold_inputs(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.renderManager.change_position((0, -self.delta_time/2))
        if pressed[pygame.K_a]:
            self.renderManager.change_position((-self.delta_time/2, 0))
        if pressed[pygame.K_s]:
            self.renderManager.change_position((0, self.delta_time/2))
        if pressed[pygame.K_d]:
            self.renderManager.change_position((self.delta_time/2, 0))


class Planet:
    def __init__(self, position: tuple[int, int], size: int):
        self.position = position
        self.size = size
        self.color = "#88DD88"
        self.rect = pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)
        self.routes: list[Route] = []

    def add_route(self, route):
        self.routes.append(route)

    def get_zoomed_position(self, zoom_level: int, surface_size: tuple[int, int]):
        return tuple(map(lambda pos: pos*zoom_level - (surface_size[0]/2)*(zoom_level-1), self.position))

    def get_render_info(self):
        return {
            "position": self.position,
            "size": self.size,
            "color": self.color
        }
        # scale_level = screen.height/map_size[0]
        # new_zoom_level = zoom_level * scale_level
        # new_position = self.get_zoomed_position(new_zoom_level, screen.size)
        # new_size = self.size * new_zoom_level
        # pygame.draw.circle(screen, self.color, new_position, new_size)


class Route:
    def __init__(self, planet1: Planet, planet2: Planet, size):
        self.planet1 = planet1
        self.planet2 = planet2
        self.size = size
        # heavenly code
        x1 = min(self.planet1.position[0]-self.planet1.size, self.planet2.position[0]-self.planet2.size)
        y1 = min(self.planet1.position[1]-self.planet1.size, self.planet2.position[1]-self.planet2.size)
        x2 = max(self.planet1.position[0]+self.planet1.size, self.planet2.position[0]+self.planet2.size)
        y2 = max(self.planet1.position[1]+self.planet1.size, self.planet2.position[1]+self.planet2.size)
        self.rect = pygame.Rect(x1, y1, x2-x1, y2-y1)

    def get_render_info(self):
        return {
            "position1": self.planet1.position,
            "position2": self.planet2.position,
            "size": self.size,
            "color": "#BBBBBB"
        }

class Map:
    def __init__(self):
        self.map_rect = None
        self.planets: list[Planet] = []
        self.routes: list[Route] = []

    def generate_map(self, map_size):
        self.map_rect = pygame.Rect(0, 0, map_size[0], map_size[1])
        planet1 = Planet((0, 0), 30)
        planet2 = Planet((300, 300), 30)
        planet3 = Planet((100, 200), 30)
        self.planets.append(planet1)
        self.planets.append(planet2)
        self.planets.append(planet3)
        self.add_route(planet1, planet2)
        self.add_route(planet1, planet3)
        self.add_route(planet2, planet3)

    def add_planet(self, position, size=30):
        planet = Planet(position, size)
        self.planets.append(planet)

    def add_route(self, planet1: Planet, planet2: Planet, size=10):
        route = Route(planet1, planet2, size)
        planet1.add_route(route)
        planet2.add_route(route)
        self.routes.append(route)


    def get_render_info(self):
        planets = []
        routes = []
        for planet in self.planets:
            planets.append(planet.get_render_info())
        for route in self.routes:
            routes.append(route.get_render_info())
        return planets, routes


class RenderManager:
    def __init__(self, map: Map):
        self.map = map
        self.zoom_level = 1
        self.viewport = pygame.Rect()

    def change_position(self, pos_amount):
        self.viewport.move_ip(pos_amount)
        print(self.viewport)

    def change_zoom(self, amount, mouse_pos, screen_size):
        self.zoom_level = self.zoom_level*(1+amount)
        self.zoom_level = max(1, min(self.zoom_level, 10))

    def render(self, map: Map, screen: pygame.Surface):
        screen.fill("#777777")
        self.viewport.width = screen.width
        self.viewport.height = screen.height
        planets, routes = map.get_render_info()
        scale_amount = screen.height/map.map_rect.height * self.zoom_level

        for route_info in routes:
            position1 = route_info["position1"]
            position1 = (position1[0]-self.viewport.left, position1[1]-self.viewport.top)
            position1 = (position1[0]*scale_amount, position1[1]*scale_amount)
            position2 = route_info["position2"]
            position2 = (position2[0]-self.viewport.left, position2[1]-self.viewport.top)
            position2 = (position2[0]*scale_amount, position2[1]*scale_amount)
            size = route_info["size"] * scale_amount
            pygame.draw.line(screen, route_info["color"], position1, position2, int(size))

        for planet_info in planets:
            position = planet_info["position"]
            position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
            position = (position[0]*scale_amount, position[1]*scale_amount)
            size = planet_info["size"] * scale_amount
            pygame.draw.circle(screen, planet_info["color"], (position[0], position[1]), size)

if __name__ == "__main__":
    game = MainGame()