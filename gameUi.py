from gameMap import Map
from planets import *

class GameUi:
    def __init__(self, timescale, paused, map: Map):
        self.__timescale = timescale
        self.__paused = paused
        self.__map = map
        self.__menu = Menu()

    def toggle_menu(self):
        self.__menu.toggle_active()

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
            "offset": (10, 10)
        })

        if self.__map.get_active():
            info.append({
            "type": "text",
            "text": f"Q - Turret Upgrade (10 Drones)\nE - Factory Upgrade ({FactoryPlanet.cost} Drones)",
            "color": "#000000",
            "size": 50,
            "position": "bottomleft",
            "offset": (10, -10)
            })

        if self.__map.alert:
            info.append({
            "type": "text",
            "text": self.__map.alert,
            "color": "#BB0000",
            "size": 50,
            "position": "bottom",
            "offset": (0, -20)
            })

        if self.__menu.get_active():
            info.extend(self.__menu.get_render_info())

        return info

class Menu:
    def __init__(self):
        self.__active = False

    def get_active(self):
        return self.__active

    def toggle_active(self):
        self.__active = not self.__active

    def get_render_info(self):
        info = []
        info.append({
            "type": "rect",
            "size": (450,450),
            "color": "#555555",
            "position": "top",
            "offset": (0,0)
        })

        info.append({
            "type": "rect",
            "size": (450,450),
            "color": "#555555",
            "position": "top",
            "offset": (0,500)
        })

        return info