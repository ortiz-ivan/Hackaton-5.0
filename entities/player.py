# entities/player.py
import pygame
import os
from config import PLAYER_SPEED

class Player:
    def __init__(self, position):
        self.position = pygame.Vector2(position)
        self.speed = PLAYER_SPEED

        # --- Carga de la imagen de Jose ---
        ruta_imagen = os.path.join("assets", "images", "Jose_frotal.png")
        
        # Definimos el tamaño que queremos que tenga Jose en el juego
        self.size = (40, 40)
        
        try:
            self.image = pygame.image.load(ruta_imagen).convert_alpha()
            # Escalamos la imagen al tamaño definido en self.size
            self.image = pygame.transform.scale(self.image, self.size)
            
        except pygame.error as e:
            print(f"Error al cargar la imagen: {e}")
            self.image = pygame.Surface(self.size)
            self.image.fill((0, 255, 0))

        # El rect se crea usando el tamaño de la imagen
        self.rect = self.image.get_rect(topleft=self.position)

        # --- Estado controlado por sistemas ---
        self.move_direction = pygame.Vector2(0, 0)
        self.want_interact = False

        # --- Nuevo estado: sentado ---
        self.is_seated = False

        # --- Cargar ícono de chatín ---
        self.chat_icon = pygame.image.load("assets/images/icons/hablando.png").convert_alpha()
        self.chat_icon_offset = pygame.Vector2(0, -30)  # Ajusta la posición del ícono

    def update_rect(self):
        """Update rect position based on current position"""
        self.rect.topleft = self.position

    def render(self, screen):
        screen.blit(self.image, self.position)
