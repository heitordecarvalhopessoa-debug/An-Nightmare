import pygame as pg
import settings as st

class History:
    def __init__(self, game):
        self.game = game
        self.font = pg.font.SysFont('arial', 28)
        self.title_font = pg.font.SysFont('arial', 45, bold=True)
        self.lines = [
            "You were called to participate in a scientific experiment",
            "involving a pill that can help the user sleep well",
            "and wake up refreshed...",
            "",
            "But something went wrong.",
            "",
            "You entered a finite nightmare where time is limited.",
            "Collect 'files' to increase your time and escape it all."
        ]
        self.line_idx = 0
        self.char_idx = 0
        self.text_timer = 0
        self.wait_timer = 0
        self.display_lines = [""] * len(self.lines)

    def update(self):
        # Lógica de máquina de escrever
        if self.line_idx < len(self.lines):
            self.text_timer += self.game.delta_time
            if self.text_timer > 0.04:  # Velocidade do surgimento das letras
                self.text_timer = 0
                current_full_line = self.lines[self.line_idx]
                
                if self.char_idx < len(current_full_line):
                    self.display_lines[self.line_idx] += current_full_line[self.char_idx]
                    self.char_idx += 1
                    self.game.sound.play_typewriter_click()
                else:
                    self.line_idx += 1
                    self.char_idx = 0
        else:
            # Quando o texto acaba, espera um pouco e entra no jogo
            self.wait_timer += self.game.delta_time
            if self.wait_timer > 2.5:
                self.start_game()

    def start_game(self):
        self.game.showing_history = False
        self.game.in_menu = False
        pg.mouse.set_visible(False)
        pg.event.set_grab(True)
        pg.mouse.get_rel()

    def draw(self):
        center_x = st.WIDTH // 2
        
        # Title
        title_render = self.title_font.render("THE EXPERIMENT", True, (150, 0, 0))
        self.game.screen.blit(title_render, (center_x - title_render.get_width() // 2, 100))

        # Story lines
        for i, line in enumerate(self.display_lines):
            if line:
                render = self.font.render(line, True, (200, 200, 200))
                self.game.screen.blit(render, (center_x - render.get_width() // 2, 220 + i * 35))

        # Dica discreta (opcional) para pular
        if self.line_idx < len(self.lines):
            prompt = pg.font.SysFont('arial', 18).render("[ENTER] TO SKIP", True, (50, 50, 50))
            self.game.screen.blit(prompt, (st.WIDTH - prompt.get_width() - 20, st.HEIGHT - 30))

    def handle_events(self, event):
        if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
            self.start_game()