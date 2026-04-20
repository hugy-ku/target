import pygame
import time
from gameMap import Map
from renderManager import RenderManager
from gameUi import GameUi
import cProfile

class MainGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((200, 200), pygame.RESIZABLE)
        self.clock = pygame.Clock()
        self.running = True
        self.delta_time = 0
        self.framerate = pygame.display.get_current_refresh_rate()
        if self.framerate == 0:
            self.framerate = 60

        self.timescale = 1
        self.paused = False

        self.map = Map()
        self.map.random_generate((2000, 2000))
        self.ui = GameUi(self.timescale, self.paused, self.map)
        self.renderManager = RenderManager(self.map, self.ui)


        self.mouse_pos = None
        self.current_time = 0
        self.time_since_last_tick = 0

        self.milliseconds_per_tick = 20

        self.mainloop()

    def mainloop(self):
        while self.running:
            self.handle_hold_inputs()

            for event in pygame.event.get():
                # print(event) # debug
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            if not self.paused:
                # convert to int in case timescale < 1 and it divides
                self.current_time += int(self.delta_time * self.timescale)
                self.time_since_last_tick += int(self.delta_time * self.timescale)

                self.tick(self.time_since_last_tick // self.milliseconds_per_tick)
                self.time_since_last_tick %= self.milliseconds_per_tick
                self.map.render_tick(self.delta_time)

            self.renderManager.render(self.screen, self.delta_time)

            pygame.display.flip()
            self.delta_time = self.clock.tick(self.framerate)


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
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.map.mousedown(event.button)
        if event.type == pygame.MOUSEBUTTONUP:
            self.map.mouseup(event.button)

        if event.type == pygame.KEYDOWN:
            timescales = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]
            if event.key in timescales:
                timescale = int(event.unicode)
                self.timescale = 2**(timescale-1) # starts from 2^0 (or 1)
                self.paused = False
                self.ui.set_paused(self.paused)
                self.ui.set_timescale(timescale)

            if event.key == pygame.K_SPACE:
                self.paused = not self.paused
                self.ui.set_paused(self.paused)

            if event.key == pygame.K_q:
                self.map.upgrade_fort()

            if event.key == pygame.K_e:
                self.map.upgrade_factory()

    def tick(self, amount=1):
        self.map.tick(amount)


if __name__ == "__main__":
    # cProfile.run("MainGame()")
    game = MainGame()