from gameMap import Map
from planets import *
import pygame

class GameUi:
    def __init__(self, timescale, paused, map: Map):
        self.__timescale = timescale
        self.__paused = paused
        self.__map = map
        self.__menu = Menu()
        self.__statistics_menu = StatisticsMenu()
        self.__end_game = False

    def mousedown(self, screen: pygame.Surface, mouse_pos, mouse_button):
        scale_amount = screen.height/1000
        mouse_pos =  (mouse_pos[0]//scale_amount, mouse_pos[1]//scale_amount)
        if self.__statistics_menu.get_active():
            return
        elif self.__menu.get_active():
            return self.__menu.mousedown(screen, mouse_pos, mouse_button)

    def handle_escape(self):
        if self.__statistics_menu.get_active():
            self.__statistics_menu.toggle_active()
            return True
        else:
            return self.__menu.toggle_active()

    def toggle_statistics_menu(self):
        return self.__statistics_menu.toggle_active()

    def new_game(self):
        self.__end_game = False
        if self.__menu.get_active():
            self.__menu.toggle_active()

    def end_game(self):
        self.__end_game = True

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
        })

        if self.__map.get_active():
            info.append({
            "type": "text",
            "text": f"Q - Turret Upgrade (10 Drones)\nE - Factory Upgrade ({FactoryPlanet.cost} Drones)",
            "color": "#000000",
            "size": 50,
            "position": "bottomleft",
            "offset": (10, -10),
            })

        if self.__map.alert:
            info.append({
            "type": "text",
            "text": self.__map.alert,
            "color": "#BB0000",
            "size": 50,
            "position": "bottom",
            "offset": (0, -20),
            })

        if self.__end_game:
            info.append({
            "type": "text",
            "text": f"Game has ended! Press space to restart",
            "color": "#000000",
            "size": 75,
            "position": "top",
            "offset": (0, 425),
            })

        if self.__menu.get_active():
            info.extend(self.__menu.get_render_info())

        if self.__statistics_menu.get_active():
            info.extend(self.__statistics_menu.get_render_info())

        return info

class Button:
    def __init__(self, position, size, color, text, text_position, text_size, text_color, anchor):
        self.position = position
        self.size = size
        self.color = color
        self.text = text
        self.text_position = text_position
        self.text_size = text_size
        self.text_color = text_color
        self.anchor = anchor

        self.__rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def in_button(self, pos):
        return self.__rect.collidepoint(pos[0], pos[1])

class Menu:
    def __init__(self):
        self.__active = False
        self.__buttons: list[Button] = []

        buttons_padding = (0, 200)
        for text in ["Resume", "Restart", "Statistics", "Exit"]:
            self.__buttons.append(Button(buttons_padding, (250,100), "#666666", text, (buttons_padding[0],buttons_padding[1]+25), 75, "#DDDDDD", "top"))
            buttons_padding = (buttons_padding[0], buttons_padding[1]+150)

    def get_active(self):
        return self.__active

    def toggle_active(self):
        self.__active = not self.__active
        return self.__active

    def mousedown(self, screen, mouse_pos, mouse_button):
        if mouse_button != 1:
            return

        width_size = 1000*screen.width/screen.height

        for button in self.__buttons:
            if button.anchor == "top":
                new_mouse_pos = (mouse_pos[0]-(width_size-button.size[0])//2, mouse_pos[1])
            if button.in_button(new_mouse_pos):
                return button.text


    def get_render_info(self):
        info = []


        for i, button in enumerate(self.__buttons):
            info.append({
                "type": "rect",
                "size": button.size,
                "color": button.color,
                "position": button.anchor,
                "offset": (button.position[0], button.position[1])
            })
            info.append({
                "type": "text",
                "text": button.text,
                "size": button.text_size,
                "color": button.text_color,
                "position": button.anchor,
                "offset": (button.text_position[0], button.text_position[1]),
            })

        return info

class StatisticsMenu:
    def __init__(self):
        self.__active = False
        self.selected = 0

    def get_active(self):
        return self.__active

    def toggle_active(self):
        self.__active = not self.__active
        return self.__active

    def mousedown(self, mouse_pos, button):
        pass

    def get_render_info(self):
        info = []

        info.append({
            "type": "text",
            "text": "testeted",
            "size": 75,
            "color": "#000000",
            "position": "top",
            "offset": (0, 25)
        })

        info.append({
            "type": "rect",
            "size": (800, 800),
            "color": "#333333",
            "position": "top",
            "offset": (0, 100)
        })

        return info