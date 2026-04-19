class GameUi:
    def __init__(self, timescale):
        self.__timescale = timescale

    def set_timescale(self, timescale):
        self.__timescale = timescale

    def get_render_info(self):
        info = []
        info.append({
            "type": "text",
            "text": f"{">"*self.__timescale}",
            "color": "#000000",
            "size": 1,
            "position": "bottomright",
            "padding": (10, 10)
        })
        return info