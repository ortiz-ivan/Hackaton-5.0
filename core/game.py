import pygame
import os
from systems.spawn_system import SpawnSystem
# ### NUEVO: Importamos tus herramientas y el sistema de movimiento
from utils.helpers import load_obstacle_data
from entities.obstacle import Obstacle
from systems.movement_system import MovementSystem

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

        # ### NUEVO: Inicializar Obstáculos
        self.obstacle_configs = load_obstacle_data()
        self.obstacles = pygame.sprite.Group()
        self._setup_obstacles() # Método para sembrar el aula

        # Sistema de spawn (Alumnos)
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(self.students)
        
        # ### NUEVO: Sistema de Movimiento (Asumiendo que self.player existe)
        # Si aún no tienes el objeto player creado, esta línea dará error.
        # self.movement_system = MovementSystem(self.player, self.obstacles)

    def _setup_obstacles(self):
        """Método para crear las sillas y mochilas iniciales."""
        if "mochila_basica" in self.obstacle_configs:
            m1 = Obstacle(200, 150, self.obstacle_configs["mochila_basica"])
            self.obstacles.add(m1)
        
        if "silla_escolar" in self.obstacle_configs:
            s1 = Obstacle(400, 300, self.obstacle_configs["silla_escolar"])
            self.obstacles.add(s1)

    def update(self, dt):
        # Actualizar alumnos
        for student in self.students:
            student.update(dt)
        
        # ### NUEVO: Actualizar obstáculos (por si las sillas se mueven)
        self.obstacles.update(dt)
        
        # ### NUEVO: Actualizar movimiento del profesor
        # self.movement_system.update(dt)

    def render(self):
        # 1️⃣ Dibujar aula
        self.screen.blit(self.background, (0, 0))

        # 2️⃣ Dibujar alumnos
        for student in self.students:
            student.render(self.screen)
            
        # ### NUEVO: 3️⃣ Dibujar obstáculos
        self.obstacles.draw(self.screen)

        pygame.display.flip()
