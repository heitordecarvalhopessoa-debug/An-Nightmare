import pygame as pg
import sys
import math
import settings as st

class Menu:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.SysFont('arial', 40, bold=True)
        self.title_font = pg.font.SysFont('arial', 80, bold=True)
        self.menu_state = 'main'
        
        self.main_options_base = ['PLAY', 'CONTROLS', 'SETTINGS', 'CREDITS', 'EXIT']
        self.settings_options = ['RESOLUTION', 'FULLSCREEN', 'SENSITIVITY', 'BACK']
        self.credits_options = ['BACK']
        self.controls_options = ['BACK']
        
        self.credits_info = [
            "      AN NIGHTMARE           ",
            "---------------------------",
            "    DEV: Heitor Pessoa    ",
            "      Engine: VSCode       ",
            "     Language: Python      "
        ]
        
        self.controls_info = [
            "WASD - MOVE",
            "SHIFT - SPRINT",
            "SPACE - JUMP",
            "MOUSE - LOOK",
            "ESC - PAUSE"
        ]

        self.selected_index = 0
        self.bg_index = 0
        self.bg_timer = 0
        self.bg_change_time = 4.0 # Segundos entre trocas de imagem

        self.res_idx = st.RES_OPTIONS.index(st.RES) if st.RES in st.RES_OPTIONS else 0
        self.sens_idx = st.SENS_OPTIONS.index(st.MOUSE_SENSITIVITY) if st.MOUSE_SENSITIVITY in st.SENS_OPTIONS else 1

    def draw_background(self):
        bg_img = self.game.textures.bg_images[self.bg_index]
        self.game.screen.blit(bg_img, (0, 0))
        
        # Overlay escuro para garantir legibilidade do texto
        overlay = pg.Surface((st.WIDTH, st.HEIGHT))
        overlay.set_alpha(170)
        overlay.fill((0, 0, 0))
        self.game.screen.blit(overlay, (0, 0))

    def draw(self):
        self.draw_background()
        center_x = st.WIDTH // 2
        
        if self.menu_state == 'main':
            current_main_options = list(self.main_options_base)
            if self.game.paused:
                current_main_options[0] = 'RESUME'

            self.draw_text_with_shadow('AN NIGHTMARE', self.title_font, (180, 0, 0), center_x, st.HEIGHT // 4)
            for i, option in enumerate(current_main_options):
                # Efeito de brilho pulsante na opção selecionada
                glow = math.sin(pg.time.get_ticks() * 0.01) * 35 + 220 if i == self.selected_index else 100
                color = (glow, 0, 0) if i == self.selected_index else (80, 80, 80)
                self.draw_text_with_shadow(option, self.font, color, center_x, st.HEIGHT // 2 + i * 55)
        
        elif self.menu_state == 'settings':
            self.draw_text_with_shadow('SETTINGS', self.title_font, (150, 0, 0), center_x, st.HEIGHT // 4)
            for i, option in enumerate(self.settings_options):
                if option == 'RESOLUTION':
                    res = st.RES_OPTIONS[self.res_idx]
                    text = f"RESOLUTION: {res[0]}x{res[1]}"
                elif option == 'FULLSCREEN':
                    status = "ON" if st.FULLSCREEN else "OFF"
                    text = f"FULLSCREEN: {status}"
                elif option == 'SENSITIVITY':
                    text = f"SENSITIVITY: {st.SENS_OPTIONS[self.sens_idx]}"
                else:
                    text = option
                
                color = (255, 255, 255) if i == self.selected_index else (80, 80, 80)
                self.draw_text_with_shadow(text, self.font, color, center_x, st.HEIGHT // 2 + i * 55)

        elif self.menu_state == 'controls':
            self.draw_text_with_shadow('CONTROLS', self.title_font, (150, 0, 0), center_x, st.HEIGHT // 4)
            for i, line in enumerate(self.controls_info):
                self.draw_text_with_shadow(line, self.font, (200, 200, 200), center_x, st.HEIGHT // 2 + i * 45)
            self.draw_text_with_shadow('BACK', self.font, (255, 255, 255), center_x, st.HEIGHT - 80)

        elif self.menu_state == 'credits':
            self.draw_text_with_shadow('CREDITS', self.title_font, (150, 0, 0), center_x, st.HEIGHT // 4)
            for i, line in enumerate(self.credits_info):
                self.draw_text_with_shadow(line, self.font, (200, 200, 200), center_x, st.HEIGHT // 2 + i * 45)
            self.draw_text_with_shadow('BACK', self.font, (255, 255, 255), center_x, st.HEIGHT - 80)

    def draw_text(self, text, font, color, x, y, align='center'):
        render = font.render(text, True, color)
        rect = render.get_rect()
        if align == 'right':
            rect.midright = (x, y)
        else:
            rect.center = (x, y)
        self.game.screen.blit(render, rect)

    def draw_text_with_shadow(self, text, font, color, x, y):
        shadow = font.render(text, True, (20, 20, 20))
        s_rect = shadow.get_rect(center=(x + 2, y + 2))
        self.game.screen.blit(shadow, s_rect)
        self.draw_text(text, font, color, x, y)

    def update(self):
        self.bg_timer += self.game.delta_time
        if self.bg_timer >= self.bg_change_time:
            self.bg_timer = 0
            self.bg_index = (self.bg_index + 1) % len(self.game.textures.bg_images)

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            current_options_list = []
            if self.menu_state == 'main':
                current_options_list = list(self.main_options_base)
                if self.game.paused:
                    current_options_list[0] = 'RESUME'
            elif self.menu_state == 'settings':
                current_options_list = self.settings_options
            elif self.menu_state == 'credits':
                current_options_list = self.credits_options
            elif self.menu_state == 'controls':
                current_options_list = self.controls_options

            if not current_options_list:
                return

            if event.key == pg.K_UP:
                self.selected_index = (self.selected_index - 1) % len(current_options_list)
                self.game.sound.play_menu_beep()
            elif event.key == pg.K_DOWN:
                self.selected_index = (self.selected_index + 1) % len(current_options_list)
                self.game.sound.play_menu_beep()
            
            elif self.menu_state == 'settings' and (event.key == pg.K_LEFT or event.key == pg.K_RIGHT):
                delta = 1 if event.key == pg.K_RIGHT else -1
                if current_options_list[self.selected_index] == 'RESOLUTION':
                    self.res_idx = (self.res_idx + delta) % len(st.RES_OPTIONS)
                    self.apply_settings()
                elif current_options_list[self.selected_index] == 'FULLSCREEN':
                    st.FULLSCREEN = not st.FULLSCREEN
                    self.apply_settings()
                elif current_options_list[self.selected_index] == 'SENSITIVITY':
                    self.sens_idx = (self.sens_idx + delta) % len(st.SENS_OPTIONS)
                    self.apply_settings()
                self.game.sound.play_menu_beep()

            elif event.key == pg.K_RETURN:
                self.game.sound.play_menu_beep()
                self.select_option()
            elif event.key == pg.K_ESCAPE and self.menu_state != 'main':
                self.menu_state = 'main'
                self.selected_index = 0

    def select_option(self):
        if self.menu_state == 'main':
            current_main_options = list(self.main_options_base)
            if self.game.paused:
                current_main_options[0] = 'RESUME'
            
            selected_option_text = current_main_options[self.selected_index]

            if selected_option_text == 'PLAY':
                self.game.showing_history = True
                self.game.history.__init__(self.game) # Reseta o estado da animação
            elif selected_option_text == 'RESUME':
                self.game.paused = False
                pg.mouse.set_visible(False)
                pg.event.set_grab(True)
            elif selected_option_text == 'CONTROLS':
                self.menu_state = 'controls'
                self.selected_index = 0
            elif selected_option_text == 'SETTINGS':
                self.menu_state = 'settings'
                self.selected_index = 0
            elif selected_option_text == 'CREDITS':
                self.menu_state = 'credits'
                self.selected_index = 0
            elif selected_option_text == 'EXIT':
                self.game.exiting = True
        
        elif self.menu_state == 'settings':
            choice = self.settings_options[self.selected_index]
            if choice == 'BACK': self.menu_state = 'main'; self.selected_index = 2
        
        elif self.menu_state in ['credits', 'controls']:
            self.menu_state = 'main'
            self.selected_index = 1 if self.menu_state == 'controls' else 3

    def apply_settings(self):
        st.MOUSE_SENSITIVITY = st.SENS_OPTIONS[self.sens_idx]
        
        new_res = st.RES_OPTIONS[self.res_idx]
        st.RES = st.WIDTH, st.HEIGHT = new_res
        
        st.NUM_RAYS = st.WIDTH // 2
        st.HALF_NUM_RAYS = st.NUM_RAYS // 2
        st.DELTA_ANGLE = st.FOV / st.NUM_RAYS
        st.SCREEN_DIST = st.HALF_NUM_RAYS / math.tan(st.HALF_FOV)
        st.SCALE = st.WIDTH // st.NUM_RAYS
        
        self.game.update_resolution()