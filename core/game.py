import pygame
import os
import random # Lo necesitaremos para el spawn aleatorio
from config import SCREEN_WIDTH, SCREEN_HEIGHT # Asegúrate de que existan

from systems.spawn_system import SpawnSystem
from utils.helpers import load_obstacle_data
from entities.obstacle import Obstacle
from systems.movement_system import MovementSystem # ### FIX: Importación añadida

class Game:
    def __init__(self, screen):
        self.screen = screen

        # Cargar fondo
        self.background = pygame.image.load(
            os.path.join("assets", "images", "aula.png")
        ).convert()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )

        # Estudiantes
        self.students = []

        # Obstáculos
        self.obstacle_configs = load_obstacle_data()
        self.obstacles = pygame.sprite.Group()
        
        # Temporizador para los 5 segundos
        self.spawn_timer = 0
        self.spawn_interval = 5.0
        self._spawn_random_obstacle() # Creamos el primero

        # Sistema de alumnos
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(self.students)
        
        # NOTA: Si self.player no existe aún, comenta la siguiente línea:
        # self.player = TuClasePlayer() 
        # self.movement_system = MovementSystem(self.player, self.obstacles)

    def _spawn_random_obstacle(self):
        #Borra el anterior y crea uno nuevo cada 5 segundos."""
        self.obstacles.empty()
        
        # Posición aleatoria
        rx = random.randint(50, SCREEN_WIDTH - 50)
        ry = random.randint(50, SCREEN_HEIGHT - 50)
        
        if "mochila_basica" in self.obstacle_configs:
            config = self.obstacle_configs["mochila_basica"]
            # Asegúrate de que Obstacle reciba (x, y, config_dict)
            nueva = Obstacle(rx, ry, config)
            self.obstacles.add(nueva)

    def update(self, dt):
        # Lógica del temporizador de 5 segundos
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self._spawn_random_obstacle()
            self.spawn_timer = 0

        # Actualizar alumnos
        for student in self.students:
            student.update(dt)
        
        # Actualizar obstáculos
        self.obstacles.update(dt)
        
        # Si activaste el movement_system, descomenta esto:
        # self.movement_system.update(dt)

    def render(self):
        self.screen.blit(self.background, (0, 0))
        for student in self.students:
            student.render(self.screen)
        
        self.obstacles.draw(self.screen)
        pygame.display.flip()