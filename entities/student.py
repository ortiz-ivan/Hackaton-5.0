import pygame
import os 
from config import STUDENT_SIZE

class Student(pygame.sprite.Sprite):
    def __init__(self, position, image_name='alumno(1).png'):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'images', image_name)).convert_alpha()
        self.image = pygame.transform.scale(self.image, STUDENT_SIZE)
        self.rect = self.image.get_rect(center=position)
        self.state = 'normal'
        
    def update(self, dt):
        pass
    
    def render (self, screen):
        screen.blit(self.image, self.rect)
        
    