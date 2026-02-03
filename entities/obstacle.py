import pygame
import os
import random


class Obstacle(pygame.sprite.Sprite):
    """Obstáculo del aula.

    Compatible con dos formas de construcción:
      - Obstacle(x, y, width, height)
      - Obstacle(x, y, config_dict)
    """

    def __init__(self, x, y, config_or_width, height=None):
        super().__init__()

        # Caso: se pasa un diccionario de configuración (from obstacles.json)
        if isinstance(config_or_width, dict):
            cfg = config_or_width
            width = cfg.get("width", 32)
            height = cfg.get("height", 32)
            self.type = cfg.get("type", "static")
            color = tuple(cfg.get("color", (100, 100, 100)))
            asset = cfg.get("asset_path")

            # Velocidad aleatoria para obstacles dinámicos
            if self.type == "dynamic":
                min_s = cfg.get("speed_min", 50)
                max_s = cfg.get("speed_max", 120)
                speed = random.uniform(min_s, max_s)
                angle = random.uniform(0, 360)
                self.velocity = pygame.Vector2()
                self.velocity.from_polar((speed, angle))
            else:
                self.velocity = pygame.Vector2(0, 0)
        else:
            # Forma clásica (width, height)
            width = config_or_width
            if height is None:
                raise TypeError("Obstacle.__init__() missing required positional argument: 'height'")
            self.type = "static"
            color = (100, 100, 100)
            asset = None
            self.velocity = pygame.Vector2(0, 0)

        # Intentamos cargar asset si existe
        if asset and os.path.exists(asset):
            try:
                img = pygame.image.load(asset).convert_alpha()
                self.image = pygame.transform.scale(img, (width, height))
            except Exception:
                self.image = pygame.Surface((width, height)).convert()
                self.image.fill(color)
        else:
            self.image = pygame.Surface((width, height)).convert()
            self.image.fill(color)

        # Rectángulo de colisión
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, dt=0):
        """Actualiza posición si es dinámico. `dt` en segundos."""
        if self.type == "dynamic":
            self.rect.x += int(self.velocity.x * dt)
            self.rect.y += int(self.velocity.y * dt)

            # Rebotar con los bordes de la pantalla
            screen_w, screen_h = pygame.display.get_surface().get_size()
            if self.rect.left < 0:
                self.rect.left = 0
                self.velocity.x *= -1
            if self.rect.right > screen_w:
                self.rect.right = screen_w
                self.velocity.x *= -1
            if self.rect.top < 0:
                self.rect.top = 0
                self.velocity.y *= -1
            if self.rect.bottom > screen_h:
                self.rect.bottom = screen_h
                self.velocity.y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect)
