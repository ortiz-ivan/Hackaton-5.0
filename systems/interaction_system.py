# systems/interaction_system.py
import pygame


class InteractionSystem:
    INTERACTION_DISTANCE = 40  # píxeles

    def __init__(self, player, input_system):
        self.player = player
        self.input_system = input_system

    def update(self, students):
        # Solo actuamos si el jugador intenta interactuar
        if not self.input_system.interact_pressed:
            return

        student = self._get_nearby_student(students)

        if student is None:
            # No hay estudiante cerca
            return

        self._handle_interaction(student)

    def _get_nearby_student(self, students):
        for student in students:
            if self._is_close(self.player, student):
                return student
        return None

    def _is_close(self, a, b):
        if hasattr(a, 'rect'):
            ax, ay = a.rect.centerx, a.rect.centery
        else:
            ax, ay = a.position.x, a.position.y
        if hasattr(b, 'rect'):
            bx, by = b.rect.centerx, b.rect.centery
        else:
            bx, by = b.position.x, b.position.y
        dx = ax - bx
        dy = ay - by
        return (dx * dx + dy * dy) ** 0.5 <= self.INTERACTION_DISTANCE

    def _handle_interaction(self, student):
        student.state = "leaving"
        student.target_position = pygame.Vector2(720, 500)  # puerta
