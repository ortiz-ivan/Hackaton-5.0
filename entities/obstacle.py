import pygame
from config import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, type="static", velocity=(0, 0)):
        super().__init__()

        # Definimos el tipo de obstáculo (mochila, silla, etc.)
        self.type = type

        # Superficie visual básica (mientras Camila entrega los assets) [cite: 11, 24]
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # Un gris temporal

        # El rect es fundamental para el movement_system que vas a crear
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        # Para obstáculos dinámicos (como sillas moviéndose)
        self.velocity = pygame.Vector2(velocity)

    def update(self):
        # Si el obstáculo es dinámico, aquí actualizamos su posición.
        if self.type == "dynamic":
            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y

            # Lógica simple de rebote con los bordes del aula
            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.velocity.x *= -1
            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.velocity.y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
