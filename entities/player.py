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
        self.rect = self.image.get_rect(topleft=self.position)

        # --- Estado controlado por sistemas ---
        self.move_direction = pygame.Vector2(0, 0)
        self.want_interact = False

    def update_rect(self):
        """Update rect position based on current position"""
        self.rect.topleft = self.position

    def render(self, screen):
        screen.blit(self.image, self.position)
