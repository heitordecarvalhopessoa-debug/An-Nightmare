import settings as st
import pygame as pg
import math

class Player:
    def __init__ (self, game):
        self.game = game
        self.x, self.y = self.game.map.player_start
        self.angle = st.PLAYER_ANGLE
        self.z = 0 # Posição vertical para o pulo
        self.jump_z = 0
        self.bob_timer = 0
        self.vel_z = 0
        self.is_jumping = False
        self.is_locked = False
        
        # Stats
        self.life = 100
        self.defense = 50

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if self.is_locked:
            pg.mouse.get_rel() # Limpa o buffer de movimento
            return

        if mx < 100 or mx > st.WIDTH - 100:
            pg.mouse.set_pos([st.WIDTH // 2, st.HEIGHT // 2])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-st.MOUSE_MAX_REL, min(st.MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * st.MOUSE_SENSITIVITY

    def movement(self):
        sin_a, cos_a = math.sin(self.angle), math.cos(self.angle)
        dx, dy = 0, 0
        
        keys = pg.key.get_pressed()
        speed = st.PLAYER_SPEED
        speed *= self.game.delta_time
        
        # Pulo
        if not self.is_jumping and pg.key.get_pressed()[pg.K_SPACE]:
            self.is_jumping = True
            self.vel_z = st.JUMP_SPEED

        speed_sin = speed * sin_a
        speed_cos = speed * cos_a
        if keys[pg.K_w]:
            dx += speed_cos
            dy += speed_sin
        if keys[pg.K_s]:
            dx += -speed_cos
            dy += -speed_sin
        if keys[pg.K_a]:
            dx += speed_sin
            dy += -speed_cos
        if keys[pg.K_d]:
            dx += -speed_sin
            dy += speed_cos

        if keys[pg.K_LEFT]:
            self.angle -= st.PLAYER_ROT_SPEED * self.game.delta_time
        if keys[pg.K_RIGHT]:
            self.angle += st.PLAYER_ROT_SPEED * self.game.delta_time

        self.check_wall_collision(dx, dy)
        
        # Head Bobbing Logic
        if (dx != 0 or dy != 0) and not self.is_jumping:
            self.bob_timer += self.game.delta_time * st.BOB_FREQ
            bob_z = math.sin(self.bob_timer) * st.BOB_AMP
        else:
            self.bob_timer = 0
            bob_z = 0
        
        self.z = self.jump_z + bob_z
        self.angle %= math.tau
        
    def check_file_collection(self):
        # File collection logic
        if self.map_pos in self.game.map.files_map:
            self.game.map.files_map.pop(self.map_pos)
            self.game.files_collected += 1
            self.game.level_timer += st.TIME_PER_FILE
            self.game.sound.play_collect_file()
            self.jump_z += 5 # Feedback visual na coleta

    def jump_logic(self):
        if self.is_jumping:
            self.jump_z += self.vel_z * self.game.delta_time
            self.vel_z -= st.GRAVITY * self.game.delta_time
            if self.jump_z < 0:
                self.jump_z = 0
                self.is_jumping = False
                self.vel_z = 0

    def check_wall(self, x, y):
        return (x, y) not in self.game.map.world_map
    
    def check_wall_collision(self, dx, dy):
        if self.check_wall(int(self.x + dx), int(self.y)):
            self.x += dx
        if self.check_wall(int(self.x), int(self.y + dy)):
            self.y += dy

    def draw(self):
        pg.draw.circle(self.game.screen, 'green', (self.x * 100, self.y * 100), 15)

    def update(self):
        self.mouse_control()
        self.movement()
        self.check_file_collection()
        self.jump_logic()

    @property
    def pos(self):
        return (self.x, self.y)

    @property
    def map_pos(self):
        return int(self.x), int(self.y)