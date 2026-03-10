import pygame
import time

class MainGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200))
        self.clock = pygame.Clock()
        self.running = True
        self.delta_time = 0
        self.renderManager = RenderManager((300,300))
        self.map = Map()
        self.map.generate_map()
        self.mainloop()

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill("#000000")
            self.renderManager.render(self.map, self.screen)
            pygame.display.flip()

            self.delta_time = self.clock.tick(60)

class Map:
    def __init__(self):
        self.planets: list[Planet] = []

    def generate_map(self):
        self.planets.append(Planet((50, 60)))

    def render(self, surface: pygame.Surface, viewport: pygame.Surface):
        # viewport for culling or something idk im doing premature optimisation im so dead
        for visible_planet in viewport.get_rect().collideobjectsall(self.planets, key=lambda o: o.rect):
            visible_planet: Planet
            visible_planet.render(surface)
        return surface

class RenderManager:
    def __init__(self, map_size: tuple):
        self.surface = pygame.Surface(map_size)
        self.viewport = self.surface.subsurface(pygame.Rect(0, 0, 100, 100))

    def render(self, map: Map, screen: pygame.Surface):
        self.surface = map.render(self.surface, self.viewport)
        pygame.transform.scale(self.viewport, screen.size, dest_surface=screen) # woah blitting by scaling this is so cool

class Planet:
    def __init__(self, position: tuple, size=10):
        self.position = position
        self.size = size
        self.color = "#88DD88"

    @property
    def rect(self):
        return pygame.Rect(self.position[0]-self.size, self.position[1]-self.size, 2*self.size, 2*self.size)

    def render(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, self.position, self.size)

game = MainGame()