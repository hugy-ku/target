from gameMap import Map

class GameUi:
    def __init__(self, timescale, paused, map: Map):
        self.__timescale = timescale
        self.__paused = paused
        self.__map = map

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
            "size": 100,
            "position": "topleft",
            "offset": (10, 10)
        })

        if self.__map.get_active():
            info.append({
            "type": "text",
            "text": "Q - Turret Upgrade (10 Drones)\nE - Factory Upgrade (10 Drones)",
            "color": "#000000",
            "size": 75,
            "position": "bottomleft",
            "offset": (10, -10)
            })

        return info