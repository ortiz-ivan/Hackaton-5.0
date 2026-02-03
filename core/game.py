import pygame
import os

from systems.spawn_system import SpawnSystem
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.interaction_system import InteractionSystem

from entities.player import Player
from entities.obstacle import Obstacle


class Game:
    def __init__(self, screen):
        self.screen = screen

        # ─────────────────────────────
        # Fondo (aula)
        # ─────────────────────────────
        self.background = pygame.image.load(
            os.path.join("assets", "images", "aula.png")
        ).convert()
        self.background = pygame.transform.scale(
            self.background, self.screen.get_size()
        )

        # ─────────────────────────────
        # Jugador
        # ─────────────────────────────
        self.player = Player((100, 100))

        # ─────────────────────────────
        # Obstáculos estáticos (mesas)
        # ─────────────────────────────
        self.obstacles = pygame.sprite.Group()
        self._setup_obstacles()

        # ─────────────────────────────
        # Sistemas
        # ─────────────────────────────
        # --- Sistema de movimiento del jugador ---
        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(self.player, self.obstacles)

        # --- Sistema de interacción ---
        self.interaction_system = InteractionSystem(self.player, self.input_system)

        # --- Estudiantes ---
        self.students = []

        # --- Sistema de spawn de estudiantes ---
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(self.students)

    # ─────────────────────────────
    # Layout del aula
    # ─────────────────────────────
    def _setup_obstacles(self):
        """
        Define las mesas del aula.
        Estos obstáculos son sólidos y bloquean el movimiento.
        """

        mesas = [
            Obstacle(92, 60, 150, 40),
            Obstacle(318, 60, 150, 40),
            Obstacle(540, 60, 150, 40),
            Obstacle(92, 147, 150, 40),
            Obstacle(318, 147, 150, 40),
            Obstacle(540, 147, 150, 40),
            Obstacle(92, 234, 150, 40),
            Obstacle(318, 234, 150, 40),
            Obstacle(540, 234, 150, 40),
            Obstacle(92, 321, 150, 40),
            Obstacle(318, 321, 150, 40),
            Obstacle(540, 320, 150, 40),
            Obstacle(92, 405, 150, 40),
            Obstacle(318, 405, 150, 40),
            Obstacle(540, 405, 150, 40),
            Obstacle(92, 490, 150, 40),
            Obstacle(318, 490, 150, 40),
            Obstacle(540, 490, 150, 40),
        ]

        for mesa in mesas:
            self.obstacles.add(mesa)

    # ─────────────────────────────
    # Update
    # ─────────────────────────────
    def update(self, dt):
        # --- Input ---
        self.input_system.update()

        # --- Movimiento (player + students) ---
        self.movement_system.update(dt, self.students)

        # --- Interacción ---
        self.interaction_system.update(self.students)

        # --- Actualizar estudiantes ---
        for student in self.students:
            student.update(dt)

        # --- Remover estudiantes que se fueron ---
        self.students = [s for s in self.students if s.state != "left"]

        # --- Spawn ---
        self.spawn_system.update(dt, self.students)

        # --- Obstáculos ---
        self.obstacles.update()

    # ─────────────────────────────
    # Render
    # ─────────────────────────────
    def render(self):
        self.screen.blit(self.background, (0, 0))

        for student in self.students:
            student.render(self.screen)

        self.obstacles.draw(self.screen)

        self.player.render(self.screen)

        pygame.display.flip()
