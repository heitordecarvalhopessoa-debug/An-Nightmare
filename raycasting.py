import pygame as pg
import math
import settings as st

class Raycasting:
    def __init__(self, game):
        self.game = game
        self.depth_buffer = [0.0] * st.NUM_RAYS
        self.fov = st.FOV
        self.screen_dist = st.SCREEN_DIST

    def draw(self):
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, side, wall_type, offset = values
            if depth > st.MAX_DEPTH:
                continue

            # Cálculo da Névoa otimizado
            fog_factor = 1.0 / (1.0 + depth * depth * 0.1)
            color_mod = int(255 * fog_factor)
            if side: color_mod = int(color_mod * 0.7)

            tint = (color_mod, color_mod, color_mod)
            if wall_type == 2: tint = (0, color_mod, 0)
            
            # Pega a coluna do Optimizer (não precisa escalar nem pintar aqui, o cache já traz pronto)
            wall_column = self.game.optimizer.get_wall_column(
                self.game.textures.wall_texture, offset, proj_height, tint
            )
            
            # Aplica o tremor no blit das paredes
            self.game.screen.blit(wall_column, (
                ray * st.SCALE + self.game.shake_h, 
                (st.HEIGHT - proj_height) // 2 + self.game.player.z + self.game.shake_v
            ))

    def draw_items(self):
        px, py = self.game.player.pos
        items = []
        for pos in self.game.map.files_map:
            ix, iy = pos[0] + 0.5, pos[1] + 0.5
            dist = math.sqrt((px - ix)**2 + (py - iy)**2)
            items.append((dist, ix, iy))
        
        # Ordenar por distância (pintar os mais longe primeiro)
        items.sort(key=lambda x: x[0], reverse=True)

        for dist, ix, iy in items:
            dx, dy = ix - px, iy - py
            theta = math.atan2(dy, dx)
            gamma = theta - self.game.player.angle
            
            if gamma > math.pi: gamma -= math.tau
            if gamma < -math.pi: gamma += math.tau
            
            if -st.HALF_FOV - 0.2 < gamma < st.HALF_FOV + 0.2:
                corrected_dist = dist * math.cos(gamma)
                # Esconde itens na névoa
                if corrected_dist < 0.2 or corrected_dist > st.MAX_DEPTH - 2: continue
                
                proj_height = self.screen_dist / (corrected_dist + 0.0001)
                screen_x = (gamma / st.FOV + 0.5) * st.WIDTH
                
                ray_idx = int(screen_x // st.SCALE)
                # Verifica se o item não está atrás de uma parede
                if 0 <= ray_idx < st.NUM_RAYS and corrected_dist < self.depth_buffer[ray_idx]:
                    file_sprite_width = int(proj_height * 0.15)
                    file_sprite_height = int(proj_height * 0.3)

                    # Efeito flutuante
                    y_off = math.sin(pg.time.get_ticks() * 0.005) * 10
                    
                    fog_val = int(255 / (1 + corrected_dist * corrected_dist * 0.1))
                    scaled_file_texture = self.game.optimizer.get_sprite(
                        self.game.textures.file_texture, file_sprite_width, file_sprite_height, (fog_val, fog_val, fog_val)
                    )

                    if scaled_file_texture:
                        # Aplica o tremor nos itens
                        self.game.screen.blit(scaled_file_texture, (
                            screen_x - file_sprite_width // 2 + self.game.shake_h, 
                            st.HEIGHT // 2 - file_sprite_height // 2 + self.game.player.z + y_off + self.game.shake_v
                        ))

    def draw_enemies(self):
        if not self.game.enemy:
            return
            
        px, py = self.game.player.pos
        # Por enquanto temos apenas um inimigo
        enemy = self.game.enemy
        ix, iy = enemy.x, enemy.y
        dist = math.hypot(ix - px, iy - py)
        
        dx, dy = ix - px, iy - py
        theta = math.atan2(dy, dx)
        gamma = theta - self.game.player.angle
        
        if gamma > math.pi: gamma -= math.tau
        if gamma < -math.pi: gamma += math.tau
        
        if -st.HALF_FOV - 0.2 < gamma < st.HALF_FOV + 0.2:
            corrected_dist = dist * math.cos(gamma)
            if corrected_dist < 0.1: return
            
            proj_height = self.screen_dist / (corrected_dist + 0.0001)
            screen_x = (gamma / st.FOV + 0.5) * st.WIDTH
            
            ray_idx = int(screen_x // st.SCALE)
            if 0 <= ray_idx < st.NUM_RAYS:
                # Verifica o depth buffer para não desenhar através de paredes
                if corrected_dist < self.depth_buffer[ray_idx]:
                    # Seleciona o conjunto de texturas e frame por tipo
                    if enemy.npc_type == 'timer':
                        images = self.game.textures.timer_images
                        frame = 0
                    elif enemy.npc_type == 'looker':
                        images = self.game.textures.looker_images
                        frame = int(enemy.frame_index) % len(images)
                    else:
                        images = self.game.textures.stalker_images
                        frame = int(enemy.frame_index) % len(images)
                    
                    texture = images[frame]

                    # Calcula largura e altura projetada
                    w = int(proj_height * enemy.size)
                    h = int(proj_height * enemy.size * 2)
                    
                    # Aplica névoa e cores especiais por tipo
                    fog_val = int(255 / (1 + corrected_dist * corrected_dist * 0.12))
                    if enemy.npc_type == 'timer':
                        # Timer agora é branco (cor original afetada apenas pela névoa)
                        tint = (fog_val, fog_val, fog_val)
                    elif enemy.npc_type == 'looker':
                        tint = (int(fog_val * 0.5), fog_val, fog_val)
                    else:
                        tint = (fog_val, int(fog_val * 0.3), int(fog_val * 0.3))
                    
                    enemy_sprite = self.game.optimizer.get_sprite(texture, w, h, tint)

                    if enemy_sprite:
                        # Aplica o tremor no inimigo
                        self.game.screen.blit(enemy_sprite, (
                            screen_x - w // 2 + self.game.shake_h, 
                            st.HEIGHT // 2 - h // 2 + self.game.player.z + self.game.shake_v
                        ))

    def ray_cast(self):
        self.ray_casting_result = []
        ox, oy = self.game.player.pos
        x_map, y_map = self.game.player.map_pos

        ray_angle = self.game.player.angle - st.HALF_FOV

        for ray in range(st.NUM_RAYS):
            sin_a = math.sin(ray_angle)
            cos_a = math.cos(ray_angle)
            sin_a = sin_a if sin_a != 0 else 1e-6
            cos_a = cos_a if cos_a != 0 else 1e-6

            # Horizontais
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - oy) / sin_a
            x_hor = ox + depth_hor * cos_a
            delta_depth = dy / sin_a
            dx = delta_depth * cos_a
            wall_type_hor = 0

            for i in range(st.MAX_DEPTH):
                tile_hor = int(x_hor), int(y_hor)
                if tile_hor in self.game.map.world_map:
                    wall_type_hor = self.game.map.world_map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # Verticais
            x_vert, dx = (x_map + 1, 1) if cos_a >= 0 else (x_map - 1e-6, -1)
            depth_vert = (x_vert - ox) / cos_a
            y_vert = oy + depth_vert * sin_a
            delta_depth = dx / cos_a
            dy = delta_depth * sin_a
            wall_type_vert = 0

            for i in range(st.MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                if tile_vert in self.game.map.world_map:
                    wall_type_vert = self.game.map.world_map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            # Profundidade
            if depth_vert < depth_hor:
                depth, side, wall_type = depth_vert, 0, wall_type_vert
                y_vert = oy + depth_vert * sin_a
                offset = y_vert % 1
            else:
                depth, side, wall_type = depth_hor, 1, wall_type_hor
                x_hor = ox + depth_hor * cos_a
                offset = x_hor % 1
            
            # Remover efeito olho de peixe usando a tabela pré-calculada
            depth *= self.game.optimizer.cos_values[ray]
            
            # Projeção 3D
            proj_height = self.screen_dist / (depth + 0.0001)

            self.ray_casting_result.append((depth, proj_height, side, wall_type, offset))
            self.depth_buffer[ray] = depth
            
            ray_angle += st.DELTA_ANGLE

    def update(self):
        self.ray_cast()