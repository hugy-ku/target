import pygame
import time
from planets import *
from gameMap import Map
from renderManager import RenderManager
from gameUi import GameUi
import cProfile
import os

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
        self.ui_paused = False
        self.game_end = False

        self.map = Map()
        self.map_size = (2000, 2000)
        self.map.new_map(self.map_size)
        self.ui = GameUi(self.timescale, self.paused, self.map)
        self.renderManager = RenderManager(self.map, self.ui)

        self.mouse_pos = None
        self.time_since_last_tick = 0
        self.milliseconds_per_tick = 20

        self.current_time = 0
        self.real_time = 0
        self.drones_created = 0
        self.drones_destroyed = 0

        self.mainloop()

    def mainloop(self):
        while self.running:
            self.real_time += self.delta_time
            self.handle_hold_inputs()

            for event in pygame.event.get():
                # print(event) # debug
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)

            if not self.paused and not self.ui_paused:
                # convert to int in case timescale < 1 and it divides
                self.current_time += int(self.delta_time * self.timescale)
                self.time_since_last_tick += int(self.delta_time * self.timescale)

                created, destroyed = self.map.tick(self.time_since_last_tick // self.milliseconds_per_tick)
                self.drones_created += created
                self.drones_destroyed += destroyed
                self.time_since_last_tick %= self.milliseconds_per_tick
                self.map.render_tick(self.delta_time)
                winner, planet_upgrades = self.map.check_win()
                if winner:
                    self.end_game(winner, planet_upgrades)

            self.renderManager.render(self.screen, self.delta_time)

            pygame.display.flip()
            self.delta_time = self.clock.tick(self.framerate)

    def new_game(self):
        self.map.new_map(self.map_size)
        self.ui.new_game()
        self.current_time = 0
        self.real_time = 0
        self.drones_created = 0
        self.drones_destroyed = 0
        self.ui_paused = False
        self.game_end = False
        self.paused = False
        self.timescale = 1

    def end_game(self, winner, planet_upgrades):
        self.game_end = True
        self.ui_paused = True
        self.ui.end_game()
        lines = []
        if not os.path.exists("statistics.csv"):
            lines.append(["winner", "gametime", "realtime", "drones_created", "drones_destroyed", "factories", "forts", "unupgraded"])
        lines.append([winner, str(self.current_time), str(self.real_time), str(self.drones_created), str(self.drones_destroyed), str(planet_upgrades[str(FactoryPlanet)]), str(planet_upgrades[str(FortPlanet)]), str(planet_upgrades[str(Planet)])])
        with open("statistics.csv", "a") as file:
            for line in lines:
                file.write(",".join(line)+"\n")

    def handle_hold_inputs(self):
        if self.ui_paused:
            return

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

        if event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        if event.type == pygame.WINDOWLEAVE:
            self.mouse_pos = None

        if self.game_end:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.key == pygame.K_ESCAPE:
                self.new_game()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.ui_paused = self.ui.handle_escape()
        if self.ui_paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                ui_event = self.ui.mousedown(self.screen, self.mouse_pos, event.button)
                if not ui_event:
                    pass
                elif ui_event == "Resume":
                    self.ui_paused = self.ui.handle_escape()
                elif ui_event == "Restart":
                    self.new_game()
                elif ui_event == "Statistics":
                    self.ui_paused = self.ui.toggle_statistics_menu()
                elif ui_event == "Exit":
                    self.running = False

        if not self.ui_paused:
            if event.type == pygame.MOUSEWHEEL:
                self.renderManager.change_zoom(event.y*0.05, pygame.mouse.get_pos())
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
                    self.map.user_upgrade_fort()

                if event.key == pygame.K_e:
                    self.map.user_upgrade_factory()


if __name__ == "__main__":
    # cProfile.run("MainGame()")
    game = MainGame()