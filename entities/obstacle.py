import pygame


class Obstacle(pygame.sprite.Sprite):
    """
    Obstáculo estático del aula (mesas, escritorios, etc.).
    Bloquea el movimiento del jugador y NPCs.
    No tiene lógica propia.
    """

    def __init__(self, x, y, width, height):
        super().__init__()

        # Superficie visual básica (placeholder)
        self.image = pygame.Surface((width, height))
        self.image.fill((100, 100, 100))  # Gris temporal

        # Rectángulo de colisión
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        """
        Obstáculo estático: no se actualiza.
        Se mantiene el método por compatibilidad con Sprite Groups.
        """
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)
