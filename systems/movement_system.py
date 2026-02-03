import pygame


class MovementSystem:
    def __init__(self, player, obstacles, screen_rect):
        self.player = player
        self.obstacles = obstacles
        self.screen_rect = screen_rect  # límites del aula

    def update(self, dt, students=None):
        # Mover jugador
        self._move_entity(self.player, dt)

        # Mover estudiantes
        if students:
            for student in students:
                self._move_entity(student, dt)

    # ─────────────────────────────
    # Movimiento genérico
    # ─────────────────────────────
    def _move_entity(self, entity, dt):
        direction = entity.move_direction

        if direction.length_squared() == 0:
            return

        displacement = direction * entity.speed * dt

        # Eje X (deslizamiento)
        if direction.x != 0:
            new_x = entity.position.x + displacement.x
            future_rect_x = pygame.Rect(new_x, entity.position.y, *entity.size)

            if not self._check_collision(future_rect_x):
                entity.position.x = new_x

        # Eje Y (deslizamiento)
        if direction.y != 0:
            new_y = entity.position.y + displacement.y
            future_rect_y = pygame.Rect(entity.position.x, new_y, *entity.size)

            if not self._check_collision(future_rect_y):
                entity.position.y = new_y

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
