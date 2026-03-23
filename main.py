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
        self.map.generate_map((700, 700))
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
            self.renderManager.render(self.map, self.screen)
            pygame.display.flip()

            self.delta_time = self.clock.tick(60)

    def handle_input(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEWHEEL:
            self.renderManager.change_zoom(event.y*0.05, self.mouse_pos, self.screen.size)

class Planet:
    def __init__(self, position: tuple, size):
        self.position = position
        self.size = size
        self.color = "#88DD88"
        self.rect = pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)
        self.routes: list[Route] = []

    def add_route(self, route):
        self.routes.append(route)

    def render(self, surface: pygame.Surface):
        pygame.draw.aacircle(surface, self.color, self.position, self.size)


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

    def render(self, surface: pygame.Surface):
        pygame.draw.line(surface, "#BBBBBB", self.planet1.position, self.planet2.position, self.size)


class Map:
    def __init__(self):
        self.map_size = None
        self.planets: list[Planet] = []
        self.routes: list[Route] = []

    def generate_map(self, map_size):
        self.map_size = map_size
        planet1 = Planet((50, 50), 30)
        planet2 = Planet((200, 50), 30)
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


    def render(self, surface: pygame.Surface, viewport: pygame.Rect):
        # viewport for culling or something idk im doing premature optimisation im so dead
        # heavenly code 2.0
        surface.fill("#777777")
        for visible_route in viewport.collideobjectsall(self.routes, key=lambda route: route.rect):
            visible_route: Route
            visible_route.render(surface)
        for visible_planet in viewport.collideobjectsall(self.planets, key=lambda planet: planet.rect):
            visible_planet: Planet
            visible_planet.render(surface)
        return surface


class RenderManager:
    def __init__(self, map: Map):
        self.surface = pygame.Surface(map.map_size)
        self.zoom_level = 1
        self.viewport_position = (0, 0)
        self.viewport = pygame.Rect()

    def change_zoom(self, amount, mouse_pos, screen_size):

        viewport_mouse = (mouse_pos[0]-(screen_size[0]-self.viewport.width*self.zoom_level)/2, mouse_pos[1]-(screen_size[1]-self.viewport.height*self.zoom_level)/2)
        if viewport_mouse[0] < 0 or viewport_mouse[1] < 0 or viewport_mouse[0] > self.viewport.width*self.zoom_level or viewport_mouse[1] > self.viewport.height*self.zoom_level:
            return

        self.zoom_level = self.zoom_level*(1+amount)
        if self.zoom_level > 10:
            self.zoom_level = 10
            return
        if self.zoom_level < 1:
            self.zoom_level = 1
            return
        self.viewport_position = (self.viewport_position[0]+viewport_mouse[0]*amount/self.zoom_level, self.viewport_position[1]+viewport_mouse[1]*amount/self.zoom_level)
        self.viewport_position = (max(0, min(self.viewport_position[0], self.surface.size[0]-self.viewport.width)), max(0, min(self.viewport_position[1], self.surface.size[1]-self.viewport.height)))
        # print(self.viewport_position[0], self.surface.size[0]-self.viewport.width)

    def render(self, map: Map, screen: pygame.Surface):
        screen.fill("#000000")
        self.viewport = pygame.Rect(0, 0, screen.size[0], screen.size[1])
        # if self.viewport.width > self.surface.width or self.viewport.height > self.surface.height:
        self.viewport = self.viewport.clip(self.surface.get_rect())
        self.viewport = self.viewport.fit(self.viewport.copy().scale_by(1/self.zoom_level))
        self.viewport.topleft = self.viewport_position
        # self.viewport.width = self.viewport.width/self.zoom_level
        # self.viewport.height = self.viewport.height/self.zoom_level
        # self.viewport.left, self.viewport.top = self.viewport_position
        # have to do this due to the ordering of processing
        self.viewport.left, self.viewport.top = (max(0, min(self.viewport_position[0], self.surface.size[0]-self.viewport.width)), max(0, min(self.viewport_position[1], self.surface.size[1]-self.viewport.height)))
        viewport_surface = self.surface.subsurface(self.viewport)
        # viewport_surface.fill("#777777")
        self.surface = map.render(self.surface, self.viewport)
        scale_ratio = min(screen.size[0]/self.viewport.width, screen.size[1]/self.viewport.height)
        scaled_viewport = pygame.transform.scale(viewport_surface, (viewport_surface.size[0]*scale_ratio, viewport_surface.size[1]*scale_ratio))
        # print(viewport_surface.size, scale_ratio, (viewport_surface.size[0]*scale_ratio, viewport_surface.size[1]*scale_ratio))
        screen.blit(scaled_viewport, ((screen.size[0]-scaled_viewport.size[0])/2, (screen.size[1]-scaled_viewport.size[1])/2))

game = MainGame()