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
        self.map.generate_map((300, 300))
        self.renderManager = RenderManager(self.map)
        self.mainloop()

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.renderManager.render(self.map, self.screen)
            pygame.display.flip()

            self.delta_time = self.clock.tick(60)

class Map:
    def __init__(self):
        self.map_size = None
        self.planets: list[Planet] = []

    def generate_map(self, map_size):
        self.map_size = map_size
        self.planets.append(Planet((50, 60)))

    def render(self, surface: pygame.Surface, viewport: pygame.Rect):
        # viewport for culling or something idk im doing premature optimisation im so dead
        for visible_planet in viewport.collideobjectsall(self.planets, key=lambda o: o.rect):
            visible_planet: Planet
            visible_planet.render(surface)
        return surface

class RenderManager:
    def __init__(self, map: Map):
        self.surface = pygame.Surface(map.map_size)
        self.viewport = pygame.Rect(0, 0, 100, 100)

    def render(self, map: Map, screen: pygame.Surface):
        screen.fill("#000000")
        viewport_surface = self.surface.subsurface(self.viewport)
        viewport_surface.fill("#777777")
        self.surface = map.render(self.surface, self.viewport)
        scale_ratio = min(screen.size[0]/self.viewport.width, screen.size[1]/self.viewport.height)
        scaled_viewport = pygame.transform.scale_by(viewport_surface, scale_ratio)
        screen.blit(scaled_viewport, ((screen.size[0]-scaled_viewport.size[0])/2, (screen.size[1]-scaled_viewport.size[1])/2))

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