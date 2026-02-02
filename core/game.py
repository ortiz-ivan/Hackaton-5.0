import pygame
import os
from systems.spawn_system import SpawnSystem
from entities.player import Player
from entities.obstacle import Obstacle
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem


class Game:
    def __init__(self, screen):
        self.screen = screen

        # --- Cargar fondo (aula) ---
        self.background = pygame.image.load(
            os.path.join("assets", "images", "aula.png")
        ).convert()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )

        # --- Crear jugador ---
        self.player = Player((100, 100))

        # --- Obstáculos estáticos ---
        self.obstacles = pygame.sprite.Group()
        
        # Temporizador para los 5 segundos
        self.spawn_timer = 0
        self.spawn_interval = 5.0
        self._spawn_random_obstacle() # Creamos el primero

        # --- Sistema de movimiento del jugador ---
        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(self.player, self.obstacles)

        # --- Estudiantes ---
        self.students = []

        # --- Obstáculos estáticos ---
        self.obstacles = pygame.sprite.Group()
        self._setup_obstacles()

        # --- Sistema de movimiento del jugador ---
        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(self.player, self.obstacles)

        # --- Estudiantes ---
        self.students = []

        # --- Sistema de spawn de estudiantes ---
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(self.students)
        
        # NOTA: Si self.player no existe aún, comenta la siguiente línea:
        # self.player = TuClasePlayer() 
        # self.movement_system = MovementSystem(self.player, self.obstacles)

    def _setup_obstacles(self):
        """Sembrar obstáculos estáticos en el aula"""
        # Definimos obstáculos directamente (width, height)
        mochila_width, mochila_height = 40, 40
        silla_width, silla_height = 50, 50

        # Crear mochilas y sillas
        m1 = Obstacle(200, 150, mochila_width, mochila_height)
        s1 = Obstacle(400, 300, silla_width, silla_height)

        self.obstacles.add(m1, s1)

    def update(self, dt):
        # --- Input y movimiento del jugador ---
        self.input_system.update()
        self.movement_system.update(dt)

        # --- Actualizar estudiantes ---
        for student in self.students:
            student.update(dt)
        
        # Actualizar obstáculos
        self.obstacles.update(dt)
        
        # Si activaste el movement_system, descomenta esto:
        # self.movement_system.update(dt)

        # --- Actualizar obstáculos (aunque ahora son estáticos) ---
        self.obstacles.update()

    def render(self):
        # --- Dibujar fondo ---
        self.screen.blit(self.background, (0, 0))

        # --- Dibujar estudiantes ---
        for student in self.students:
            student.render(self.screen)

        # --- Dibujar obstáculos ---
        self.obstacles.draw(self.screen)

        # --- Dibujar jugador ---
        self.player.render(self.screen)

        pygame.display.flip()
