# entities/player.py
import pygame
from config import PLAYER_SPEED


class Player:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.speed = PLAYER_SPEED

        self.size = (40, 40)
        self.image = pygame.Surface(self.size)
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(int(self.position.x), int(self.position.y)))

        # --- Estado controlado por sistemas ---
        self.move_direction = pygame.Vector2(0, 0)
        self.want_interact = False

    def render(self, screen):
        # keep rect in sync with position
        self.rect.topleft = (int(self.position.x), int(self.position.y))
        screen.blit(self.image, self.rect.topleft)
