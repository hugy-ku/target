import random
import math

class Drone:
    def __init__(self, position, color, offset=0, angle_offset=0, size=4):
        self.color = color
        self.position = position
        self.target_position = position
        self.offset = offset
        self.angle_offset = angle_offset
        self.size = size

    def set_target(self, new_position):
        self.target_position = new_position

    def tick(self, delta_time):
        self.position = (self.position[0]+(self.target_position[0]-self.position[0])*(1-1/2**(delta_time/50)), self.position[1]+(self.target_position[1]-self.position[1])*(1-1/2**(delta_time/50)))

    def get_render_info(self):
        return {
            "position": self.position,
            "color": self.color,
            "size": self.size
        }