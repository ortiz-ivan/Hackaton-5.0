import pygame
import os
import math


class PowerUp:
    TYPES = ["speed", "attention", "patience", "freeze", "calm", "slow"]

    SIZE = 40
    LIFE_TIME = 15.0

    def __init__(self, type, position):
        self.type = type
        self.position = pygame.Vector2(position)
        self.rect = pygame.Rect(position[0], position[1], self.SIZE, self.SIZE)
        self.active = True

        self.remaining_time = self.LIFE_TIME

        # Animación de pulso
        self.pulse_timer = 0
        self.pulse_speed = 3.0

        # Cargar sprite
        self.sprite = self._load_sprite()

    def _load_sprite(self):
        """Carga el sprite del powerup, con fallback si no existe el archivo."""
        path = os.path.join("assets", "images", "powerups", f"{self.type}.png")

        try:
            image = pygame.image.load(path).convert_alpha()
            return pygame.transform.scale(image, (self.SIZE, self.SIZE))
        except FileNotFoundError:
            # Fallback: círculo simple para no crashear si falta la imagen
            surf = pygame.Surface((self.SIZE, self.SIZE), pygame.SRCALPHA)
            pygame.draw.circle(
                surf,
                (255, 255, 255),
                (self.SIZE // 2, self.SIZE // 2),
                self.SIZE // 2,
                2,
            )
            return surf

    def update(self, dt):
        if not self.active:
            return

        self.pulse_timer += dt * self.pulse_speed
        self.remaining_time -= dt

        if self.remaining_time <= 0:
            self.active = False

    def render(self, screen):
        if not self.active:
            return

        pulse = abs(math.sin(self.pulse_timer)) * 4
        size = self.SIZE + int(pulse)

        sprite_scaled = pygame.transform.scale(
            self.sprite, (size, size)
        )

        rect = sprite_scaled.get_rect(center=self.rect.center)
        screen.blit(sprite_scaled, rect)
