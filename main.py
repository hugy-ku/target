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
        self.map.generate_map((2000, 2000))
        self.renderManager = RenderManager(self.map)
        self.mouse_pos = None

        self.mainloop()

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                print(event) # debug
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)
            self.handle_hold_inputs()
            self.tick()
            self.renderManager.render(self.screen, self.delta_time)
            pygame.display.flip()

            self.delta_time = self.clock.tick(60)

    def handle_input(self, event: pygame.event.Event):

        if event.type == pygame.MOUSEWHEEL:
            self.renderManager.change_zoom(event.y*0.05, pygame.mouse.get_pos())
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos

    def handle_hold_inputs(self):
        pressed = pygame.key.get_pressed()

        speed_mod = 1
        if pressed[pygame.K_LSHIFT]:
            speed_mod *= 4
        if pressed[pygame.K_LCTRL]:
            speed_mod *= 0.25
        if pressed[pygame.K_w]:
            self.renderManager.change_position((0, -self.delta_time/2*speed_mod))
        if pressed[pygame.K_a]:
            self.renderManager.change_position((-self.delta_time/2*speed_mod, 0))
        if pressed[pygame.K_s]:
            self.renderManager.change_position((0, self.delta_time/2*speed_mod))
        if pressed[pygame.K_d]:
            self.renderManager.change_position((self.delta_time/2*speed_mod, 0))

        if self.mouse_pos:
            map_mouse_pos = self.renderManager.convert_mouse_pos(self.mouse_pos)
            self.map.check_hover(map_mouse_pos)

    def tick(self):
        pass


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
        self.active = None
        self.hover = None

    def check_hover(self, map_mouse_pos):
        for planet in self.planets:
            if planet.rect.collidepoint(map_mouse_pos):
                self.hover = planet
                return
        self.hover = None

    def generate_map(self, map_size):
        self.map_rect = pygame.Rect(0, 0, map_size[0], map_size[1])
        planet1 = Planet((0, 0), 100)
        planet2 = Planet((2000, 2000), 100)
        planet3 = Planet((1000, 1500), 100)
        self.planets.append(planet1)
        self.planets.append(planet2)
        self.planets.append(planet3)
        self.add_route(planet1, planet2)
        self.add_route(planet1, planet3)
        self.add_route(planet2, planet3)

    def add_planet(self, position, size=100):
        planet = Planet(position, size)
        self.planets.append(planet)

    def add_route(self, planet1: Planet, planet2: Planet, size=30):
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

        if self.hover:
            hover_info = self.hover.get_render_info()
        else:
            hover_info = None

        return {
            "planets": planets,
            "routes": routes,
            "hover": hover_info,
            "active": None
        }


class RenderManager:
    def __init__(self, map: Map):
        self.map = map
        self.zoom_level = 1
        self.viewport = map.map_rect.copy()

    def change_position(self, pos_amount):
        self.viewport.move_ip(pos_amount)

    def change_zoom(self, zoom_amount, mouse_pos):
        map_mouse_pos = self.convert_mouse_pos(mouse_pos)
        zoom_before = self.zoom_level
        self.zoom_level = self.zoom_level*(1+zoom_amount)
        self.zoom_level = max(0.5, min(self.zoom_level, 5))
        if self.zoom_level == zoom_before:
            return

        new_map_mouse_pos = self.convert_mouse_pos(mouse_pos)
        self.viewport.left -= new_map_mouse_pos[0]-map_mouse_pos[0]
        self.viewport.top -= new_map_mouse_pos[1]-map_mouse_pos[1]
        print(map_mouse_pos, self.convert_mouse_pos(mouse_pos))

    def convert_mouse_pos(self, mouse_pos):
        # mouse_x uses height because viewport is scaled by height and width would be including OOB parts
        mouse_x = (mouse_pos[0]/self.zoom_level*(self.map.map_rect.width/self.viewport.height)) + self.viewport.left
        mouse_y = (mouse_pos[1]/self.zoom_level*(self.map.map_rect.height/self.viewport.height)) + self.viewport.top
        # print(mouse_x, mouse_y)
        return mouse_x, mouse_y

    def render(self, screen: pygame.Surface, deltatime):
        screen.fill("#777777")
        self.viewport.width = screen.width
        self.viewport.height = screen.height
        render_info = self.map.get_render_info()
        scale_amount = screen.height/self.map.map_rect.height * self.zoom_level

        for route_info in render_info["routes"]:
            position1 = route_info["position1"]
            position1 = (position1[0]-self.viewport.left, position1[1]-self.viewport.top)
            position1 = (position1[0]*scale_amount, position1[1]*scale_amount)
            position2 = route_info["position2"]
            position2 = (position2[0]-self.viewport.left, position2[1]-self.viewport.top)
            position2 = (position2[0]*scale_amount, position2[1]*scale_amount)
            size = route_info["size"] * scale_amount
            pygame.draw.line(screen, route_info["color"], position1, position2, int(size))

        for planet_info in render_info["planets"]:
            position = planet_info["position"]
            position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
            position = (position[0]*scale_amount, position[1]*scale_amount)
            size = planet_info["size"] * scale_amount
            pygame.draw.circle(screen, planet_info["color"], (position[0], position[1]), size)

        if render_info["hover"]:
            planet_info = render_info["hover"]
            position = planet_info["position"]
            position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
            position = (position[0]*scale_amount, position[1]*scale_amount)
            size = planet_info["size"] * scale_amount
            pygame.draw.circle(screen, "#AAAAAA", (position[0], position[1]), size*1.25, int(size*0.125))

if __name__ == "__main__":
    game = MainGame()