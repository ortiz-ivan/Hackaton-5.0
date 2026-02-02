import pygame
import os

from systems.spawn_system import SpawnSystem
from utils.helpers import load_obstacle_data
from entities.obstacle import Obstacle


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

        # Obstáculos estáticos
        self.obstacle_configs = load_obstacle_data()
        self.obstacles = pygame.sprite.Group()
        self._setup_obstacles()

        # Sistema de spawn de alumnos
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(self.students)

    def _setup_obstacles(self):
        """Crea las sillas y mochilas iniciales del aula."""
        if "mochila_basica" in self.obstacle_configs:
            config = self.obstacle_configs["mochila_basica"]
            m1 = Obstacle(200, 150, config["width"], config["height"])
            self.obstacles.add(m1)

        if "silla_escolar" in self.obstacle_configs:
            config = self.obstacle_configs["silla_escolar"]
            s1 = Obstacle(400, 300, config["width"], config["height"])
            self.obstacles.add(s1)

    def update(self, dt):
        for student in self.students:
            student.update(dt)

    def render(self):
        # Dibujar fondo
        self.screen.blit(self.background, (0, 0))

        # Dibujar alumnos
        for student in self.students:
            student.render(self.screen)

        # Dibujar obstáculos
        self.obstacles.draw(self.screen)

        pygame.display.flip()
