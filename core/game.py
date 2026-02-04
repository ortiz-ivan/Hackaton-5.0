import pygame
import os

from systems.spawn_system import SpawnSystem
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.interaction_system import InteractionSystem

from entities.player import Player
from entities.obstacle import Obstacle
from entities.student import Student
from ui.hud import HUD  # <--- NUEVO: Importamos tu HUD

class Game:
    def __init__(self, screen):
        self.screen = screen

        # ─────────────────────────────
        # Configuración del Juego (Reglas)
        # ─────────────────────────────
        self.hud = HUD(screen)
        
        self.lives = 3              # 3 Vidas (Corazones)
        self.total_time = 120.0     # 2 Minutos de partida
        
        self.life_timer = 30.0      # Cuenta regresiva para perder vida
        self.max_life_timer = 30.0  # Para dibujar la barra
        
        self.score = 0
        self.is_game_over = False
        self.game_won = False

        # ─────────────────────────────
        # Fondo (aula)
        # ─────────────────────────────
        try:
            self.background = pygame.image.load(
                os.path.join("assets", "images", "aula.png")
            ).convert()
            self.background = pygame.transform.scale(
                self.background, self.screen.get_size()
            )
        except:
            # Fallback por si no carga la imagen
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill((56, 142, 60)) # Verde aula

        # ─────────────────────────────
        # Jugador
        # ─────────────────────────────
        self.player = Player((100, 100))

        # ─────────────────────────────
        # Obstáculos estáticos (mesas)
        # ─────────────────────────────
        self.obstacles = pygame.sprite.Group()
        self.spawn_timer = 0
        self.spawn_interval = 5.0

        # ─────────────────────────────
        # Sistemas
        # ─────────────────────────────
        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(
            self.player, self.obstacles, self.screen.get_rect()
        )
        self.interaction_system = InteractionSystem(self.player, self.input_system)

        # ─────────────────────────────
        # Layout de asientos (Tal cual lo tenías)
        # ─────────────────────────────
        self.seats = [
            pygame.Vector2(125, 80), pygame.Vector2(350, 80), pygame.Vector2(575, 80),
            pygame.Vector2(125, 167), pygame.Vector2(350, 167), pygame.Vector2(575, 167),
            pygame.Vector2(125, 254), pygame.Vector2(350, 254), pygame.Vector2(575, 254),
            pygame.Vector2(125, 341), pygame.Vector2(350, 341), pygame.Vector2(575, 341),
            pygame.Vector2(125, 428), pygame.Vector2(350, 428), pygame.Vector2(575, 428),
            pygame.Vector2(125, 515), pygame.Vector2(350, 515), pygame.Vector2(575, 515),
        ]
        self.seat_occupied = [False] * len(self.seats)

        self.exit_position = pygame.Vector2(720, 500)

        # ─────────────────────────────
        # Estudiantes
        # ─────────────────────────────
        self.students = []
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(
            self.students,
            get_free_seat=self._get_free_seat,
            exit_position=self.exit_position,
        )

        self._setup_obstacles()

    def _setup_obstacles(self):
        mesas = [
            Obstacle(92, 60, 140, 40), Obstacle(318, 60, 140, 40), Obstacle(540, 60, 140, 40),
            Obstacle(92, 147, 140, 40), Obstacle(318, 147, 140, 40), Obstacle(540, 147, 140, 40),
            Obstacle(92, 234, 140, 40), Obstacle(318, 234, 140, 40), Obstacle(540, 234, 140, 40),
            Obstacle(92, 321, 140, 40), Obstacle(318, 321, 140, 40), Obstacle(540, 320, 140, 40),
            Obstacle(92, 405, 140, 40), Obstacle(318, 405, 140, 40), Obstacle(540, 405, 140, 40),
            Obstacle(92, 490, 140, 40), Obstacle(318, 490, 140, 40), Obstacle(540, 490, 140, 40),
        ]
        for mesa in mesas:
            self.obstacles.add(mesa)

    def _get_free_seat(self):
        for i, occupied in enumerate(self.seat_occupied):
            if not occupied:
                self.seat_occupied[i] = True
                return self.seats[i], i
        return None, None

    # ─────────────────────────────
    # Lógica de Interacción (NUEVO)
    # ─────────────────────────────
    def alumno_calmado(self):
        """ Se llama cuando atiendes a un alumno """
        self.score += 100
        # Ganamos 5 segundos, pero sin pasar del máximo de 30
        self.life_timer = min(self.max_life_timer, self.life_timer + 5.0)

    # ─────────────────────────────
    # Update
    # ─────────────────────────────
    def update(self, dt):
        # --- 1. Gestión de Tiempos y Vidas (NUEVO) ---
        
        # Reloj Global (2 minutos)
        if self.total_time > 0:
            self.total_time -= dt
            if self.total_time <= 0:
                self.total_time = 0
                self.game_won = True
                # Aquí podrías detonar la victoria en main.py

        # Reloj de Vida (30 segundos)
        if not self.game_won:
            self.life_timer -= dt
            if self.life_timer <= 0:
                self.lives -= 1           # Perdemos una vida
                self.life_timer = 30.0    # Reiniciamos el reloj
                if self.lives <= 0:
                    self.is_game_over = True # Fin del juego

        # --- 2. Sistemas Existentes ---
        self.input_system.update()
        self.movement_system.update(dt, self.students)
        
        # OJO: Aquí deberías pasar 'self' o un callback a interaction_system
        # para que pueda llamar a 'self.alumno_calmado()' cuando haya éxito.
        self.interaction_system.update(self.students)

        # Actualizar estudiantes
        for student in self.students:
            student.update(dt, self.obstacles, self.students, self._get_free_seat)
            if student.state == "left" and student.seat_index is not None:
                self.seat_occupied[student.seat_index] = False

        self.students = [s for s in self.students if s.state != "left"]

        self.spawn_system.update(
            dt,
            self.students,
            get_free_seat=self._get_free_seat,
            exit_position=self.exit_position,
        )

        self.obstacles.update()

    # ─────────────────────────────
    # Render
    # ─────────────────────────────
    def render(self):
        # 1. Fondo
        self.screen.blit(self.background, (0, 0))

        # 2. Entidades
        for student in self.students:
            student.render(self.screen)
        self.obstacles.draw(self.screen)
        self.player.render(self.screen)

        # 3. HUD (Interfaz) - Dibuja encima de todo
        self.hud.render(
            chaos_current=self.life_timer,  # Barra verde
            chaos_max=self.max_life_timer,
            score=self.score,
            lives=self.lives,               # Corazones
            total_time=self.total_time      # Reloj global
        )

    