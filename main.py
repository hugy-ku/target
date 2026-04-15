import pygame
import time
from gameMap import Map
from renderManager import RenderManager

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
        self.current_time = 0
        self.time_since_last_tick = 0

        self.mainloop()

    def mainloop(self):
        while self.running:
            self.current_time += self.delta_time
            self.time_since_last_tick += self.delta_time

            self.handle_hold_inputs()

            for event in pygame.event.get():
                print(event) # debug
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            self.tick()

            self.renderManager.render(self.screen, self.current_time)

            pygame.display.flip()
            self.delta_time = self.clock.tick(60)


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

    def handle_input(self, event: pygame.event.Event):

        if event.type == pygame.MOUSEWHEEL:
            self.renderManager.change_zoom(event.y*0.05, pygame.mouse.get_pos())
        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        if event.type == pygame.WINDOWLEAVE:
            self.mouse_pos = None
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.map.check_active()

    def tick(self):
        self.map.tick()


if __name__ == "__main__":
    game = MainGame()