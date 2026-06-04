import pygame as pg
import math
import random
import sys
import settings as st

class NPC:
    def __init__(self, game, npc_type='stalker'):
        self.game = game
        self.npc_type = npc_type
        self.x, self.y = self.get_random_walkable_pos()
        self.size = 0.8
        self.teleport_timer = 0
        
        # Configurações baseadas no tipo
        self.teleport_interval = 4.0 if npc_type == 'looker' else 2.5
        self.damage_rate = 40 if npc_type == 'looker' else 25
        self.frame_index = random.randint(0, 2)
        self.animation_speed = 6.0
        if npc_type == 'timer':
            self.game.player.is_locked = False
            self.speed = 1.5 # Agora ele é lento e inevitável (Player tem 4.5)
            self.animation_speed = 5.0
            # Forçar spawn no canto inferior direito do mapa atual
            self.x = len(self.game.map.mini_map[0]) - 1.5
            self.y = len(self.game.map.mini_map) - 1.5

    def get_random_walkable_pos(self):
        map_data = self.game.map.mini_map
        rows = len(map_data)
        cols = len(map_data[0])
        while True:
            y = random.randint(0, rows - 1)
            x = random.randint(0, cols - 1)
            if map_data[y][x] in [False, 3, 4]:
                px, py = self.game.player.pos
                if math.hypot(x + 0.5 - px, y + 0.5 - py) > 3:
                    return x + 0.5, y + 0.5

    def update(self):
        if self.npc_type == 'timer':
            # Perseguição direta e rápida
            px, py = self.game.player.pos
            dx, dy = px - self.x, py - self.y
            dist = math.hypot(dx, dy)
            
            # Efeito de tremor de tela baseado na proximidade
            if dist < 6.0:
                intensity = (6.0 - dist) * 2  # Tremor reduzido para ser "pequeno"
                self.game.shake_v = random.uniform(-intensity, intensity)
                self.game.shake_h = random.uniform(-intensity, intensity)
            else:
                self.game.shake_v = self.game.shake_h = 0

            if dist > 0.3:
                self.x += (dx / dist) * self.speed * self.game.delta_time
                self.y += (dy / dist) * self.speed * self.game.delta_time
            else:
                print("YoU iLl Be BaCk")
                self.game.sound.play_nightmare_alert()
                pg.quit()
                sys.exit()
        else:
            self.teleport_timer += self.game.delta_time
            if self.teleport_timer >= self.teleport_interval:
                self.x, self.y = self.get_random_walkable_pos()
                self.teleport_timer = 0

        self.frame_index += self.animation_speed * self.game.delta_time

        self.apply_logic()

    def apply_logic(self):
        px, py = self.game.player.pos
        dx, dy = self.x - px, self.y - py
        dist = math.hypot(dx, dy)

        if dist > st.MAX_DEPTH:
            return

        theta = math.atan2(dy, dx)
        gamma = theta - self.game.player.angle
        if gamma > math.pi: gamma -= math.tau
        if gamma < -math.pi: gamma += math.tau

        # Se estiver no campo de visão (0.3 radianos ~ 17 graus)
        if abs(gamma) < 0.3:
            ray_idx = int((gamma / st.FOV + 0.5) * st.NUM_RAYS)
            if 0 <= ray_idx < st.NUM_RAYS:
                if dist < self.game.raycasting.depth_buffer[ray_idx]:
                    # Apenas o 'stalker' (seeker) dá dano ao olhar
                    if self.npc_type == 'stalker':
                        self.game.player.life = max(0, self.game.player.life - self.damage_rate * self.game.delta_time)
                    
                    if self.npc_type == 'looker':
                        self.game.player.angle = theta # Trava a visão no inimigo
                        self.game.player.is_locked = True
        elif self.npc_type == 'looker':
            self.game.player.is_locked = False