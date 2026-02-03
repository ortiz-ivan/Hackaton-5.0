import pygame
import os
import random

from utils.helpers import load_obstacle_data
from systems.spawn_system import SpawnSystem
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.interaction_system import InteractionSystem

from entities.player import Player
from entities.obstacle import Obstacle
from entities.student import Student


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

        # Temporizador para los 5 segundos
        self.spawn_timer = 0
        self.spawn_interval = 5.0
        self._spawn_random_obstacle() # Creamos el primero

        # ─────────────────────────────
        # Sistemas
        # ─────────────────────────────
        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(
            self.player, self.obstacles, self.screen.get_rect()
        )
        self.interaction_system = InteractionSystem(self.player, self.input_system)

        # ─────────────────────────────
        # Layout de asientos
        # ─────────────────────────────
        self.seats = [
            pygame.Vector2(125, 80),
            pygame.Vector2(350, 80),
            pygame.Vector2(575, 80),
            pygame.Vector2(125, 167),
            pygame.Vector2(350, 167),
            pygame.Vector2(575, 167),
            pygame.Vector2(125, 254),
            pygame.Vector2(350, 254),
            pygame.Vector2(575, 254),
            pygame.Vector2(125, 341),
            pygame.Vector2(350, 341),
            pygame.Vector2(575, 341),
            pygame.Vector2(125, 428),
            pygame.Vector2(350, 428),
            pygame.Vector2(575, 428),
            pygame.Vector2(125, 515),
            pygame.Vector2(350, 515),
            pygame.Vector2(575, 515),
        ]
        self.seat_occupied = [False] * len(self.seats)

        # Salida de los NPCs
        self.exit_position = pygame.Vector2(-50, 100)

        # ─────────────────────────────
        # Estudiantes
        # ─────────────────────────────
        self.students = []

        # ─────────────────────────────
        # Sistema de spawn de estudiantes
        # ─────────────────────────────
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(
            self.students,
            get_free_seat=self._get_free_seat,
            exit_position=self.exit_position,
        )

    # ─────────────────────────────
    # Layout del aula
    # ─────────────────────────────
    def _setup_obstacles(self):
        mesas = [
            Obstacle(92, 60, 140, 40),
            Obstacle(318, 60, 140, 40),
            Obstacle(540, 60, 140, 40),
            Obstacle(92, 147, 140, 40),
            Obstacle(318, 147, 140, 40),
            Obstacle(540, 147, 140, 40),
            Obstacle(92, 234, 140, 40),
            Obstacle(318, 234, 140, 40),
            Obstacle(540, 234, 140, 40),
            Obstacle(92, 321, 140, 40),
            Obstacle(318, 321, 140, 40),
            Obstacle(540, 320, 140, 40),
            Obstacle(92, 405, 140, 40),
            Obstacle(318, 405, 140, 40),
            Obstacle(540, 405, 140, 40),
            Obstacle(92, 490, 140, 40),
            Obstacle(318, 490, 140, 40),
            Obstacle(540, 490, 140, 40),
        ]
        for mesa in mesas:
            self.obstacles.add(mesa)

    def _spawn_random_obstacle(self):
        """Crea un obstáculo aleatorio usando data/obstacles.json si está disponible."""
        configs = load_obstacle_data()
        if not configs:
            return
        cfg = random.choice(list(configs.values()))
        width = cfg.get("width", 32)
        height = cfg.get("height", 32)
        screen_rect = self.screen.get_rect()
        x = random.randint(0, max(0, screen_rect.width - width))
        y = random.randint(0, max(0, screen_rect.height - height))
        ob = Obstacle(x, y, width, height)
        self.obstacles.add(ob)

    # ─────────────────────────────
    # Obtener asiento libre
    # ─────────────────────────────
    def _get_free_seat(self):
        for i, occupied in enumerate(self.seat_occupied):
            if not occupied:
                self.seat_occupied[i] = True
                return self.seats[i], i  # Retorna asiento y su índice
        return None, None

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
            student.update(dt, self.obstacles, self.students, self._get_free_seat)

            # Liberar asiento si el estudiante se fue
            if student.state == "left" and student.seat_index is not None:
                self.seat_occupied[student.seat_index] = False

        # --- Remover estudiantes que se fueron ---
        self.students = [s for s in self.students if s.state != "left"]

        # --- Spawn dinámico ---
        self.spawn_system.update(
            dt,
            self.students,
            get_free_seat=self._get_free_seat,
            exit_position=self.exit_position,
        )

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
