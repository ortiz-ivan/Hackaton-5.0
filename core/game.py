import pygame
import os
from systems.spawn_system import SpawnSystem

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

    def update(self, dt):
        for student in self.students:
            student.update(dt)

    def render(self):
        # 1️⃣ Dibujar aula
        self.screen.blit(self.background, (0, 0))

        # 2️⃣ Dibujar alumnos
        for student in self.students:
            student.render(self.screen)

        pygame.display.flip()
