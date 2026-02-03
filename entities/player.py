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

        # --- Estado controlado por sistemas ---
        self.move_direction = pygame.Vector2(0, 0)
        self.want_interact = False

        # --- Nuevo estado: sentado ---
        self.is_seated = False

        # --- Cargar ícono de chatín ---
        self.chat_icon = pygame.image.load("assets/images/icons/hablando.png").convert_alpha()
        self.chat_icon_offset = pygame.Vector2(0, -30)  # Ajusta la posición del ícono

    def render(self, screen):
        # Dibujar al jugador
        screen.blit(self.image, self.position)

        # Si está sentado, dibujar el ícono encima
        if self.is_seated:
            icon_pos = self.position + self.chat_icon_offset
            screen.blit(self.chat_icon, icon_pos)
