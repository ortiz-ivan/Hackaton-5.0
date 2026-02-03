import pygame
import os
from systems.spawn_system import SpawnSystem
from systems.powerup_system import PowerUpSystem  
from entities.powerup import PowerUp 

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Cargar fondo (aula)
        self.background = pygame.image.load(
            os.path.join("assets", "images", "aula.png")
        ).convert()

        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )

        # Estudiantes
        self.students = []

        # Sistema de spawn
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(self.students)
        
        #power-ups 
        self.powerups = [
            PowerUp("speed", (200, 200)),
            PowerUp("attention", (400, 300)),
            PowerUp("patience", (600, 400)),  
            PowerUp("freeze", (300, 500))
        ]
        self.powerup_system = PowerUpSystem()
        

    def update(self, dt):
        for student in self.students:
            student.update(dt)
        
        self.powerup_system.update(self.powerups, dt)
        

    def render(self):
        # 1️⃣ Dibujar aula
        self.screen.blit(self.background, (0, 0))

        # 2️⃣ Dibujar alumnos
        for student in self.students:
            student.render(self.screen)
            
        # 3️⃣ Dibujar power-ups 
        for pu in self.powerups:
            pu.draw(self.screen)

        pygame.display.flip()
