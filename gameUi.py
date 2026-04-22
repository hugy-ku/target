from gameMap import Map
from planets import *
import pygame

class GameUi:
    def __init__(self, timescale, paused, map: Map):
        self.__timescale = timescale
        self.__paused = paused
        self.__map = map
        self.__menu = Menu()

    def mousedown(self, screen: pygame.Surface, mouse_pos, mouse_button):
        mouse_pos =  (mouse_pos[0]*1000//screen.width, mouse_pos[1]*1000//screen.height)
        if not self.__menu.get_active: return
        return self.__menu.mousedown(mouse_pos, mouse_button)


    def toggle_menu(self):
        return self.__menu.toggle_active()

    def set_timescale(self, timescale):
        self.__timescale = timescale

    def set_paused(self, paused):
        self.__paused = paused

    def get_render_info(self):
        info = []
        info.append({
            "type": "text",
            "text": f"{">"*self.__timescale if not self.__paused else 'paused'}",
            "color": "#000000",
            "size": 50,
            "position": "topleft",
            "offset": (10, 10),
            "center": True
        })

        if self.__map.get_active():
            info.append({
            "type": "text",
            "text": f"Q - Turret Upgrade (10 Drones)\nE - Factory Upgrade ({FactoryPlanet.cost} Drones)",
            "color": "#000000",
            "size": 50,
            "position": "bottomleft",
            "offset": (10, -10),
            "center": True
            })

        if self.__map.alert:
            info.append({
            "type": "text",
            "text": self.__map.alert,
            "color": "#BB0000",
            "size": 50,
            "position": "bottom",
            "offset": (0, -20),
            "center": True
            })

        if self.__menu.get_active():
            info.extend(self.__menu.get_render_info())

        return info

class Button:
    def __init__(self, position, size, color, text, text_position, text_size, text_color):
        self.position = position
        self.size = size
        self.color = color
        self.text = text
        self.text_position = text_position
        self.text_size = text_size
        self.text_color = text_color

        self.__rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def in_button(self, pos):
        return self.__rect.collidepoint(pos[0], pos[1])

class Menu:
    def __init__(self):
        self.__active = False
        self.__buttons: list[Button] = []

        buttons_padding = (375, 200)
        for text in ["Resume", "Restart", "Statistics", "Exit"]:
            self.__buttons.append(Button(buttons_padding, (250,100), "#666666", text, (buttons_padding[0]+125,buttons_padding[1]+25), 75, "#DDDDDD"))
            buttons_padding = (buttons_padding[0], buttons_padding[1]+150)

    def get_active(self):
        return self.__active

    def toggle_active(self):
        self.__active = not self.__active
        return self.__active

    def mousedown(self, mouse_pos, mouse_button):
        if mouse_button != 1:
            return
        for button in self.__buttons:
            if button.in_button(mouse_pos):
                return button.text


    def get_render_info(self):
        info = []


        for i, button in enumerate(self.__buttons):
            info.append({
                "type": "rect",
                "size": button.size,
                "color": button.color,
                "position": "top",
                "offset": (0, button.position[1])
            })
            info.append({
                "type": "text",
                "text": button.text,
                "size": button.text_size,
                "color": button.text_color,
                "position": "top",
                "offset": (0, button.text_position[1]),
                "center": False
            })

        return info