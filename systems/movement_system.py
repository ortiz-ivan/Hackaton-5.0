# systems/movement_system.py
import pygame

class MovementSystem:
    def __init__(self, player, obstacles, screen_rect):
        self.player = player
        self.obstacles = obstacles
        self.screen_rect = screen_rect

    def update(self, dt, students):
        self._move_entity(self.player, dt, is_player=True)
        self.player.update_rect()  # Sincronizar rect después de mover

        # Mover estudiantes
        if students:
            for student in students:
                self._move_entity(student, dt, is_player=False)

    def _move_entity(self, entity, dt, is_player=False):
        if entity.move_direction.length_squared() == 0:
            return

        velocity = entity.move_direction * entity.speed * dt
        
        # --- Obtener dimensiones de forma segura ---
        # Si tiene .size lo usa, si no, usa el ancho/alto de su .rect
        width = entity.size[0] if hasattr(entity, 'size') else entity.rect.width
        height = entity.size[1] if hasattr(entity, 'size') else entity.rect.height

        # --- MOVIMIENTO EN X ---
        next_x = entity.position.x + velocity.x
        future_rect_x = pygame.Rect(next_x, entity.position.y, width, height)
        
        collision_x = False
        for obs in self.obstacles:
            if future_rect_x.colliderect(obs.rect):
                collision_x = True
                break
        
        if not collision_x and self.screen_rect.contains(future_rect_x):
            entity.position.x = next_x

        # --- MOVIMIENTO EN Y ---
        next_y = entity.position.y + velocity.y
        future_rect_y = pygame.Rect(entity.position.x, next_y, width, height)
        
        collision_y = False
        for obs in self.obstacles:
            if future_rect_y.colliderect(obs.rect):
                collision_y = True
                break
        
        if not collision_y and self.screen_rect.contains(future_rect_y):
            entity.position.y = next_y

        # Sincronizar el rect visual con la posición lógica
        if hasattr(entity, 'rect'):
            entity.rect.topleft = (entity.position.x, entity.position.y)