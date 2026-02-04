import pygame


class Obstacle(pygame.sprite.Sprite):
    """
    Obstáculo estático del aula (mesas, escritorios, etc.).
    Bloquea el movimiento del jugador y NPCs.
    No tiene lógica propia.
    """

    def __init__(self, x, y, width, height):
        super().__init__()

# 1. Creamos la superficie con soporte para transparencia (SRCALPHA)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        
        # 2. La llenamos con un color totalmente transparente (0, 0, 0, 0)
        # El cuarto valor (el alfa) en 0 significa 100% transparente.
        self.image.fill((0, 0, 0, 0))

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
