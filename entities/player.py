import pygame
from config import PLAYER_SPEED

class Player:
    def __init__(self, posicion):
        self.posicion = pygame.Vector2(posicion)
        self.velocidad = PLAYER_SPEED
        self.size = (40, 40)
        self.imagen = pygame.Surface(self.size)
        self.imagen.fill((0, 255, 0))  # Green for player

    def update(self, dt, direction):
        self.posicion += direction * self.velocidad * dt

    def render(self, screen):
        screen.blit(self.imagen, self.posicion)

