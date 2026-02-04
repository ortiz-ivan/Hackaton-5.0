import pygame
import os

from systems.spawn_system import SpawnSystem
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.interaction_system import InteractionSystem

from entities.player import Player
from entities.obstacle import Obstacle
from entities.student import Student

# NOTA: Ya no importamos HUD aquí. El HUD vive en main.py.

class Game:
    def __init__(self, screen):
        self.screen = screen

        # ─────────────────────────────
        # Configuración del Juego
        # ─────────────────────────────
        # Eliminamos self.lives, self.timers y self.hud. 
        # Ahora Game solo se preocupa de la lógica del aula.
        
        self.score = 0
        
        # Bandera para avisar a main.py que hubo una interacción
        self.interaction_success = False 
        self.cooldown_interaction = 0.0 # Para evitar "metralleta" de espacio

        # ─────────────────────────────
        # Fondo (aula)
        # ─────────────────────────────
        try:
            path = os.path.join("assets", "images", "aula.png")
            self.background = pygame.image.load(path).convert()
            self.background = pygame.transform.scale(self.background, self.screen.get_size())
        except:
            self.background = pygame.Surface(self.screen.get_size())
            self.background.fill((56, 142, 60)) # Verde aula

        # ─────────────────────────────
        # Jugador y Entidades
        # ─────────────────────────────
        self.player = Player((100, 100))

        self.obstacles = pygame.sprite.Group()
        self._setup_obstacles()

        # ─────────────────────────────
        # Sistemas
        # ─────────────────────────────
        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(self.player, self.obstacles, self.screen.get_rect())
        self.interaction_system = InteractionSystem(self.player, self.input_system)

        # ─────────────────────────────
        # Configuración de Asientos y Alumnos
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

        self.students = []
        self.spawn_system = SpawnSystem()
        self.spawn_system.spawn_initial(
            self.students,
            get_free_seat=self._get_free_seat,
            exit_position=self.exit_position,
        )

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
    # UPDATE
    # ─────────────────────────────
    def update(self, dt):
        # 1. Actualizar cooldown (para no interactuar 60 veces por seg)
        if self.cooldown_interaction > 0:
            self.cooldown_interaction -= dt

        # 2. Sistemas
        self.input_system.update()
        self.movement_system.update(dt, self.students)
        
        # Actualizar lógica de estudiantes
        for student in self.students:
            student.update(dt, self.obstacles, self.students, self._get_free_seat)
            if student.state == "left" and student.seat_index is not None:
                self.seat_occupied[student.seat_index] = False
        
        # Eliminar estudiantes que se fueron
        self.students = [s for s in self.students if s.state != "left"]

        # Spawnear nuevos
        self.spawn_system.update(dt, self.students, get_free_seat=self._get_free_seat, exit_position=self.exit_position)
        self.obstacles.update()

        # 3. DETECTAR INTERACCIÓN
        # Aquí verificamos si el jugador presiona espacio y activamos la bandera
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_SPACE] and self.cooldown_interaction <= 0:
            # Usamos tu sistema de interacción existente
            # interaction_system.update normalmente devuelve algo, 
            # pero asumiremos que modifica el estado del estudiante.
            
            # Verificamos manualmente colisión para activar la bandera
            interacted = False
            player_rect = self.player.rect
            
            for student in self.students:
                # Si el estudiante está esperando y lo tocamos
                if student.state == "waiting" and player_rect.colliderect(student.rect):
                    # ¡ÉXITO!
                    student.resolve_request() # Método hipotético que cambia su estado a 'calmado' o 'leaving'
                    interacted = True
                    break # Solo uno a la vez
            
            if interacted:
                self.interaction_success = True
                self.cooldown_interaction = 0.5 # Esperar medio segundo antes de la próxima

    # ─────────────────────────────
    # RENDER
    # ─────────────────────────────
    def render(self):
        # 1. Fondo
        self.screen.blit(self.background, (0, 0))

        # 2. Entidades
        # Ordenamos por posición Y para dar sensación de profundidad (opcional)
        all_sprites = sorted(self.students + [self.player], key=lambda s: s.rect.bottom)
        
        self.obstacles.draw(self.screen)
        
        for sprite in all_sprites:
            sprite.render(self.screen)

        # ¡IMPORTANTE! 
        # YA NO DIBUJAMOS EL HUD AQUÍ.
        # main.py se encarga de dibujar el HUD encima de todo esto.