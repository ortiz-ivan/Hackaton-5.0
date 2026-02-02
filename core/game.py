import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT

from core.state_manager import StateManager
from core.clock import GameClock
from entities.player import Player
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.interaction_system import InteractionSystem
from systems.spawn_system import SpawnSystem
from systems.chaos_system import ChaosSystem


class Game:
    def __init__(self, screen):
        self.screen = screen

        self.state_manager = StateManager(self)
        self.clock = GameClock()

        self.player = Player((400, 300))
        self.students = []
        self.obstacles = []

        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(self.player, self.obstacles, self.input_system)
        self.interaction_system = InteractionSystem(self.player)
        self.spawn_system = SpawnSystem()
        self.chaos_system = ChaosSystem()

        # Load background image
        self.background = pygame.image.load(os.path.join('assets', 'images', 'aula.png')).convert()
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def update(self, dt: float) -> bool:
        self.clock.update(dt)

        if self.state_manager.is_game_over():
            return False
        self.input_system.update()
        self.movement_system.update(dt, self.students)
        self.spawn_system.update(dt, self.clock.spawn_interval, self.students)
        self.interaction_system.update(self.students)
        self.chaos_system.update(dt, self.clock.chaos_multiplier, self.students)

        return True

    def render(self):
        self.screen.blit(self.background, (0, 0))

        self.player.render(self.screen)

        for student in self.students:
            student.render(self.screen)

        for obstacle in self.obstacles:
            obstacle.render(self.screen)

        self.state_manager.render(self.screen)

        pygame.display.flip()
