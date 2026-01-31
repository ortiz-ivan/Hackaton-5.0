import pygame
from core.state_manager import StateManager
from systems.input_system import InputSystem
from systems.movement_system import MovementSystem
from systems.interaction_system import InteractionSystem
from systems.spawn_system import SpawnSystem
from systems.chaos_system import ChaosSystem
from entities.player import Player


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.state_manager = StateManager(self)
        self.player = Player((400, 300))

        self.input_system = InputSystem(self.player)
        self.movement_system = MovementSystem(self.player)
        self.interaction_system = InteractionSystem(self.player)
        self.spawn_system = SpawnSystem()
        self.chaos_system = ChaosSystem()

        self.students = []

    def update(self, dt):
        self.input_system.update()
        self.movement_system.update(dt, self.students)
        self.spawn_system.update(dt, self.students)
        self.interaction_system.update(dt, self.students)
        self.chaos.update(dt, self.students)

        return not self.state_manager.is_game_over()

    def render(self):
        self.screen.fill((200, 200, 200))
        self.player.render(self.screen)
        for student in self.students:
            student.render(self.screen)
        self.state_manager.render(self.screen)
        pygame.display.flip()
