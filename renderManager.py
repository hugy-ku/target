import pygame
from gameMap import Map
from gameUi import GameUi
import math

class RenderManager:
    def __init__(self, map: Map, ui: GameUi):
        self.map = map
        self.ui = ui
        self.zoom_level = 1
        self.viewport = map.map_rect.copy()
        self.current_time = 0

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

    def circle_arc(self, screen, color, position, radius, width, arcs, arc_length, angle):
        gap_length = ((2*math.pi) - arc_length*arcs) / arcs
        for arc in range(arcs):
            pygame.draw.arc(
                screen,
                color,
                pygame.Rect(position[0]-radius, position[1]-radius, radius*2, radius*2),
                arc*(gap_length+arc_length)-angle,
                arc*(gap_length+arc_length)-angle+arc_length,
                width
            )

    def render(self, screen: pygame.Surface, delta_time):
        # the reason why the code in this function is awful is because i
        # intentionally interact with it as little as possible
        # im NOT going through viewport hell again
        self.current_time += delta_time
        screen.fill("#777777")
        self.viewport.width = screen.width
        self.viewport.height = screen.height
        map_info = self.map.get_render_info()
        scale_amount = screen.height/self.map.map_rect.height * self.zoom_level

        for route_info in map_info["routes"]:
            position1 = route_info["position1"]
            position1 = (position1[0]-self.viewport.left, position1[1]-self.viewport.top)
            position1 = (position1[0]*scale_amount, position1[1]*scale_amount)
            position2 = route_info["position2"]
            position2 = (position2[0]-self.viewport.left, position2[1]-self.viewport.top)
            position2 = (position2[0]*scale_amount, position2[1]*scale_amount)
            route_size = route_info["size"]//3 * scale_amount
            pygame.draw.line(screen, route_info["color"], position1, position2, int(route_size))

            for drones in route_info["drones"]:
                for drone in drones["visible_drones"]:
                    drone_info = drone.get_render_info()
                    position = drone_info["position"]
                    position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
                    position = (position[0]*scale_amount, position[1]*scale_amount)
                    size = drone_info["size"] * scale_amount
                    pygame.draw.circle(screen, drone_info["color"], (position[0], position[1]), size)

        for planet_info in map_info["planets"]:

            for drone in planet_info["drones"]:
                drone_info = drone.get_render_info()
                position = drone_info["position"]
                position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
                position = (position[0]*scale_amount, position[1]*scale_amount)
                size = drone_info["size"] * scale_amount
                pygame.draw.circle(screen, drone_info["color"], (position[0], position[1]), size)

            position = planet_info["position"]
            position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
            position = (position[0]*scale_amount, position[1]*scale_amount)
            size = planet_info["size"] * scale_amount
            pygame.draw.circle(screen, planet_info["color"], (position[0], position[1]), size)
            font = pygame.font.Font(None, int(size))
            font_size = font.size(str(planet_info["amount"]))
            screen.blit(font.render(str(planet_info["amount"]), False, "#000000"), (position[0]-font_size[0]/2, position[1]-font_size[1]/2))


        ##### planet selection rendering

        if map_info["hover"]:
            planet_info = map_info["hover"]
            position = planet_info["position"]
            position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
            position = (position[0]*scale_amount, position[1]*scale_amount)
            size = planet_info["size"] * scale_amount
            pygame.draw.circle(screen, "#AAAAAA", (position[0], position[1]), size*1.25, int(size*0.125))

        if map_info["active"]:
            planet_info = map_info["active"]
            position = planet_info["position"]
            position = (position[0]-self.viewport.left, position[1]-self.viewport.top)
            position = (position[0]*scale_amount, position[1]*scale_amount)
            size = planet_info["size"] * scale_amount
            self.circle_arc(screen, "#AAAAAA", position, size*1.5, int(size*0.15), 4, 1, self.current_time*0.00125)

        # UI rendering

        ui_infos = self.ui.get_render_info()
        for ui_info in ui_infos:
            if ui_info["type"] == "text":
                font = pygame.font.Font(None, int(size/self.zoom_level))
                font_size = font.size(ui_info["text"])

                if ui_info["position"] == "bottomright":
                    position = list(screen.size)
                    position[0] += ui_info["offset"][0] - font_size[0]
                    position[1] += ui_info["offset"][1] - font_size[1]

                screen.blit(font.render(ui_info["text"], False, ui_info["color"]), position)