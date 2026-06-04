import pygame as pg
import settings as st

class Textures:
    def __init__(self, game):
        self.game = game
        self.wall_texture = self.load_texture('d:/Usuario/Desktop/The OX/.assets/wall.png')
        self.file_texture = self.load_texture('d:/Usuario/Desktop/The OX/.assets/paper.png')
        self.stalker_images = [
            self.load_texture(f'd:/Usuario/Desktop/The OX/.assets/Stalker/Stalker{i}.enemy.png')
            for i in range(1, 4)
        ]
        self.looker_images = [
            self.load_texture(f'd:/Usuario/Desktop/The OX/.assets/Looker/Looker{i}.png')
            for i in range(1, 4)
        ]
        self.timer_images = [self.load_texture('d:/Usuario/Desktop/The OX/.assets/Timer/timer.png')]

        # Backgrounds para o Menu (Sequência: 1, 2, 5, 4, 3)
        self.bg_images = [
            self.load_texture(f'd:/Usuario/Desktop/The OX/.assets/Backgrounds/bg{i}.png', st.RES)
            for i in [1, 2, 5, 4, 3]
        ]

    def load_texture(self, path, res=(st.TEXTURE_SIZE, st.TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)