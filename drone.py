import random
import math

class Drone:
    def __init__(self, position, color, offset=0, angle_offset=0, size=5):
        self.color = color
        self.position = position
        self.offset = offset
        self.angle_offset = angle_offset
        self.size = size

    def set_position(self, new_position):
        self.position = new_position

    def get_render_info(self):
        return {
            "position": self.position,
            "color": self.color,
            "size": self.size
        }