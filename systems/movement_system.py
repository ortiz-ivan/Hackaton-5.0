# systems/movement_system.py
import pygame


class MovementSystem:
    def __init__(self, player, obstacles):
        self.player = player
        self.obstacles = obstacles

    def update(self, dt):
        direction = self.player.move_direction

        if direction.length_squared() == 0:
            return

        displacement = direction * self.player.speed * dt
        new_position = self.player.position + displacement

        future_rect = pygame.Rect(new_position.x, new_position.y, *self.player.size)

        # Colisión simple con obstáculos
        for obstacle in self.obstacles:
            if future_rect.colliderect(obstacle.rect):
                return  # bloquea el movimiento

        self.player.position = new_position
