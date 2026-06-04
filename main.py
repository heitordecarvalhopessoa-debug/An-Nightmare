import pygame as pg
import sys

import settings as st
from map import *
from player import *
from raycasting import *
from menu import *
from textures import *
from npc import *
from optimizer import *
from history import *
from sounds import *

class Game: 
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(st.RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.paused = False
        self.in_menu = True
        self.showing_history = False
        self.current_level = 0
        self.files_collected = 0
        self.total_files = 0
        self.level_transition = False
        self.pause_index = 0
        self.transition_timer = 0
        self.shake_v = 0
        self.shake_h = 0
        self.exiting = False
        self.level_timer = st.LEVEL_TIME
        self.exit_alpha = 0
        pg.mouse.set_visible(True)
        pg.event.set_grab(False)
        self.font = pg.font.SysFont('arial', 100, bold=True)
        self.ui_font = pg.font.SysFont('arial', 25, bold=True)
        self.optimizer = Optimizer(self)
        self.textures = Textures(self)
        self.menu = Menu(self)
        self.history = History(self)
        self.sound = Sound(self)
        self.new_game()

    def new_game(self):
        self.files_collected = 0
        self.map = Map(self)
        self.player = Player(self)
        self.raycasting = Raycasting(self)
        self.level_timer = st.LEVEL_TIME
        self.last_timer_val = st.LEVEL_TIME

        if self.current_level == 7: # Nível 8 (O Vazio)
            self.enemy = NPC(self, npc_type='timer')
        elif self.current_level >= 2: # Level 3+ (índice 2 em diante)
            self.enemy = NPC(self, npc_type='looker')
        else:
            self.enemy = NPC(self, npc_type='stalker')

    def next_level(self):
        self.current_level += 1
        if self.current_level >= len(MAP_DATA):
            self.current_level = 0
            self.in_menu = True
            pg.mouse.set_visible(True)
            pg.event.set_grab(False)
        self.new_game()

    def update_resolution(self):
        flags = pg.FULLSCREEN if st.FULLSCREEN else 0
        self.screen = pg.display.set_mode(st.RES, flags)
        # Recria o optimizer para atualizar as tabelas trigonométricas com a nova resolução
        self.optimizer = Optimizer(self)
        self.raycasting = Raycasting(self)
        self.new_game()
        
    def update(self):
        if self.exiting:
            self.exit_alpha += 350 * self.delta_time
            if self.exit_alpha >= 255:
                pg.quit()
                sys.exit()
            return

        if self.in_menu:
            if self.showing_history:
                self.history.update()
            self.menu.update()
        elif self.level_transition:
            pass
        elif not self.paused:
            self.shake_v = 0
            self.shake_h = 0
            self.level_timer -= self.delta_time

            # Som de relógio quando faltar 10 segundos
            if self.level_timer <= 10 and int(self.level_timer) < int(self.last_timer_val):
                self.sound.play_clock_ticking()
            self.last_timer_val = self.level_timer

            # Se o tempo acabar, teleporta para o "Limbo" (Nível 8)
            if self.level_timer <= 0 and self.current_level != 7:
                self.sound.play_nightmare_alert()
                self.current_level = 7
                self.new_game()

            self.player.update()
            self.raycasting.update()
            if self.enemy:
                self.enemy.update()
            # Trigger transition only if items exist and all are collected
            if self.total_files > 0 and self.files_collected >= self.total_files:
                self.level_transition = True
        self.delta_time = self.clock.tick(st.FPS) / 1000
        pg.display.set_caption(f'{self.clock.get_fps():.1f}')

    def draw_ui(self):
        # Stats in top right
        ui_bg = pg.Surface((210, 150))
        ui_bg.set_alpha(150)
        ui_bg.fill('black')
        self.screen.blit(ui_bg, (st.WIDTH - 220 + self.shake_h, 10 + self.shake_v))
        
        timer_color = 'white' if self.level_timer > 10 else 'red'
        timer_txt = self.ui_font.render(f"TIME: {max(0, int(self.level_timer))}", True, timer_color)
        life_txt = self.ui_font.render(f"LIFE: {self.player.life}", True, 'red')
        def_txt = self.ui_font.render(f"DEF: {self.player.defense}", True, 'blue')
        files_txt = self.ui_font.render(f"FILES: {self.files_collected}/{self.total_files}", True, 'cyan')
        lvl_name = "?" if self.current_level == 7 else self.current_level + 1
        lvl_txt = self.ui_font.render(f"LEVEL: {lvl_name}", True, 'white')
        
        self.screen.blit(timer_txt, (st.WIDTH - 210 + self.shake_h, 20 + self.shake_v))
        self.screen.blit(life_txt, (st.WIDTH - 210 + self.shake_h, 40 + self.shake_v))
        self.screen.blit(def_txt, (st.WIDTH - 210 + self.shake_h, 60 + self.shake_v))
        self.screen.blit(files_txt, (st.WIDTH - 210 + self.shake_h, 80 + self.shake_v))
        self.screen.blit(lvl_txt, (st.WIDTH - 210 + self.shake_h, 100 + self.shake_v))

    def draw(self):
        if self.in_menu:
            self.screen.fill('black')
            if self.showing_history:
                self.history.draw()
            else:
                self.menu.draw()
        elif self.paused:
            # Desenha o mundo ao fundo mas com um overlay escuro
            self.draw_game_background()
            overlay = pg.Surface((st.WIDTH, st.HEIGHT))
            overlay.set_alpha(200)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
            self.menu.draw_text('PAUSED', self.font, (150, 0, 0), st.WIDTH // 2, st.HEIGHT // 4)
            
            options = ['RESUME', 'QUIT TO MENU']
            for i, opt in enumerate(options):
                color = (255, 255, 255) if i == self.pause_index else (80, 80, 80)
                prefix = "> " if i == self.pause_index else "  "
                self.menu.draw_text(f"{prefix}{opt}", self.menu.font, color, st.WIDTH // 2, st.HEIGHT // 2 + i * 60)

        elif self.level_transition:
            self.screen.fill((5, 5, 25))
            glow = math.sin(pg.time.get_ticks() * 0.005) * 55 + 200
            render = self.font.render('LEVEL COMPLETED', True, (glow, glow, 0))
            rect = render.get_rect(center=(st.WIDTH // 2, st.HEIGHT // 2 - 60))
            self.screen.blit(render, rect)
            
            msg = self.ui_font.render(f"FILES DECRYPTED: {self.files_collected} / {self.total_files}", True, 'white')
            self.screen.blit(msg, (st.WIDTH // 2 - msg.get_width() // 2, st.HEIGHT // 2 + 20))
            
            if (pg.time.get_ticks() // 500) % 2:
                prompt = self.ui_font.render('PRESS [ENTER] TO UPLOAD DATA AND CONTINUE', True, 'cyan')
                self.screen.blit(prompt, (st.WIDTH // 2 - prompt.get_width() // 2, st.HEIGHT // 2 + 100))
        else:
            self.draw_game_background()
            self.draw_ui()

        if self.exiting:
            exit_surf = pg.Surface(st.RES)
            exit_surf.set_alpha(int(self.exit_alpha))
            exit_surf.fill((150, 0, 0))
            self.screen.blit(exit_surf, (0, 0))

        # Versão do Jogo (Canto superior esquerdo)
        version_render = self.ui_font.render("0.1 BETA", True, (100, 100, 100))
        self.screen.blit(version_render, (15, 15))

        pg.display.flip()

    def draw_game_background(self):
        self.screen.fill('black')
        # Desenha Teto e Chão com cores sólidas (Performance Máxima)
        horizon = st.HEIGHT // 2 + self.player.z
        pg.draw.rect(self.screen, (40, 40, 40), (0, 0, st.WIDTH, horizon)) 
        pg.draw.rect(self.screen, (20, 20, 20), (0, horizon, st.WIDTH, st.HEIGHT))

        self.raycasting.draw()
        self.raycasting.draw_items()
        self.raycasting.draw_enemies()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.exiting = True
            
            if self.exiting:
                continue
            
            if self.in_menu:
                if self.showing_history:
                    self.history.handle_events(event)
                else:
                    self.menu.handle_input(event)
                continue

            if self.paused:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        self.paused = False
                        pg.mouse.set_visible(False)
                        pg.event.set_grab(True)
                        pg.mouse.get_rel()
                    elif event.key == pg.K_UP:
                        self.pause_index = (self.pause_index - 1) % 2
                    elif event.key == pg.K_DOWN:
                        self.pause_index = (self.pause_index + 1) % 2
                    elif event.key == pg.K_RETURN:
                        if self.pause_index == 0: # Resume
                            self.paused = False
                            pg.mouse.set_visible(False)
                            pg.event.set_grab(True)
                            pg.mouse.get_rel()
                        else: # Quit to Menu
                            self.paused = False
                            self.in_menu = True
                            self.showing_history = False
                            pg.mouse.set_visible(True)
                            pg.event.set_grab(False)
                            self.menu.menu_state = 'main'
                            self.menu.selected_index = 0
                continue

            if self.level_transition:
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    self.level_transition = False
                    self.next_level()
                continue

            # Ativa o pause durante o jogo
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.paused = True
                pg.mouse.set_visible(True)
                pg.event.set_grab(False)
                self.pause_index = 0

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    game = Game()
    game.run()