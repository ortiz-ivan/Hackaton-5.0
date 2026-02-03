import pygame


class InputSystem:
    def __init__(self, player):
        self.player = player

    def update(self):
        keys = pygame.key.get_pressed()

        # --- Movimiento ---
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            direction.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            direction.x += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            direction.y -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            direction.y += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.player.move_direction = direction

        # --- Interacción ---
        self.interact_pressed = keys[pygame.K_e]
