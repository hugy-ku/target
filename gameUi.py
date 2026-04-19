class GameUi:
    def __init__(self, timescale, paused):
        self.__timescale = timescale
        self.__paused = paused

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
            "size": 1,
            "position": "bottomright",
            "offset": (-10, -10)
        })
        return info