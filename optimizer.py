import pygame as pg
import math
import settings as st

class Optimizer:
    def __init__(self, game):
        self.game = game
        self.texture_cache = {}
        self.sprite_cache = {}
        self.cos_values = [math.cos(st.DELTA_ANGLE * i - st.HALF_FOV) for i in range(st.NUM_RAYS)]

    def get_sprite(self, texture, w, h, color_tint):

        w, h = int(w), int(h)
        if w < 1 or h < 1: return None

        r, g, b = [(c // 16) * 16 for c in color_tint]
        
        key = (texture, w, h, (r, g, b))
        if key not in self.sprite_cache:
            if len(self.sprite_cache) > 2000:
                self.sprite_cache.clear()
            
            scaled = pg.transform.scale(texture, (w, h))
            scaled.fill((r, g, b), special_flags=pg.BLEND_MULT)
            self.sprite_cache[key] = scaled
        return self.sprite_cache[key]

    def get_wall_column(self, texture, offset, height, color_tint):
        tex_x = int(offset * (st.TEXTURE_SIZE - 1))
        h = int(height)
        h = max(1, min(h, st.HEIGHT * 2))
        
        r, g, b = [(c // 8) * 8 for c in color_tint]
        
        key = (tex_x, h, (r, g, b))
        if key not in self.texture_cache:
            if len(self.texture_cache) > 3000:
                self.texture_cache.clear()
            
            column = texture.subsurface(tex_x, 0, 1, st.TEXTURE_SIZE)
            scaled = pg.transform.scale(column, (st.SCALE, h))
            scaled.fill((r, g, b), special_flags=pg.BLEND_MULT)
            self.texture_cache[key] = scaled
        
        return self.texture_cache[key]
    