import pygame


class MovementSystem:
    def __init__(self, player, obstacles, screen_rect):
        self.player = player
        self.obstacles = obstacles
        self.screen_rect = screen_rect  # límites del aula

    def update(self, dt, students=None):
        # Mover jugador
        self._move_entity(self.player, dt, is_player=True)

        # Mover estudiantes
        if students:
            for student in students:
                self._move_entity(student, dt, is_player=False)

    # ─────────────────────────────
    # Movimiento genérico
    # ─────────────────────────────
    def _move_entity(self, entity, dt, is_player=False):
        # --- Determinar dirección ---
        if is_player:
            direction = entity.move_direction
        else:
            direction = entity.target_position - entity.position

        if direction.length_squared() == 0:
            return

        direction = direction.normalize()
        displacement = direction * entity.speed * dt

        # --- Eje X ---
        if direction.x != 0:
            new_x = entity.position.x + displacement.x
            if is_player:
                future_rect_x = pygame.Rect(new_x, entity.position.y, *entity.size)
            else:
                future_rect_x = entity.rect.copy()
                future_rect_x.centerx = new_x

            if not self._check_collision(future_rect_x):
                entity.position.x = new_x
                if not is_player:
                    entity.rect.centerx = new_x

        # --- Eje Y ---
        if direction.y != 0:
            new_y = entity.position.y + displacement.y
            if is_player:
                future_rect_y = pygame.Rect(entity.position.x, new_y, *entity.size)
            else:
                future_rect_y = entity.rect.copy()
                future_rect_y.centery = new_y

            if not self._check_collision(future_rect_y):
                entity.position.y = new_y
                if not is_player:
                    entity.rect.centery = new_y

    # ─────────────────────────────
    # Colisiones
    # ─────────────────────────────
    def _check_collision(self, rect):
        # Obstáculos (mesas)
        for obstacle in self.obstacles:
            if rect.colliderect(obstacle.rect):
                return True

        # Límites del aula
        if not self.screen_rect.contains(rect):
            return True

        return False
