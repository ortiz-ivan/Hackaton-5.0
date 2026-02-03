import pygame
import time

class PowerUp:
    def __init__(self, tipo, position, duracion=5):
        self.tipo = tipo           # "speed", "attention", "patience", "freeze"
        self.position = position
        self.duracion = duracion
        self.active = True
        
        #Difinimos la imagen segun el tipo de powerup

        self.image = pygame.Surface((32, 32))
        if tipo == "speed":
            self.image.fill((255, 0, 0))
        elif tipo == "attention":
            self.image.fill((0, 255, 0))
        elif tipo == "patience":
            self.image.fill((0, 0, 255))
        elif tipo == "freeze":
            self.image.fill((255, 255, 0))

        self.rect = self.image.get_rect(topleft=position)
        self.start_time = None

    #definimos el metodo activate para activar el powerup
    def activate(self):
        self.start_time = time.time()
        self.active = False
        
    #definimos el metodo is_expired para verificar si el powerup ha expirado
    def is_expired(self):
        if self.start_time is None:
            return False
        return (time.time() - self.start_time) >= self.duracion
    
    #definimos el metodo draw para dibujar el powerup en la pantalla
    def draw(self, screen):
        if self.active:
            screen.blit(self.image, self.rect.topleft)
