import pygame


class InteractionSystem:
    INTERACTION_DISTANCE = 40  # píxeles

    def __init__(self, player, input_system, chaos_system=None, on_interaction=None):
        self.player = player
        self.input_system = input_system
        self.chaos_system = chaos_system  # opcional, puede ser None
        self.on_interaction = on_interaction  # callback cuando hay interacción

    def update(self, students):
        # Solo actuamos si el jugador intenta interactuar
        if not self.input_system.interact_pressed:
            return

        student = self._get_nearby_student(students)
        if student is None:
            return  # No hay estudiante cerca

        self._handle_interaction(student)

    def _get_nearby_student(self, students):
        for student in students:
            if self._is_close(self.player, student):
                return student
        return None

    def _is_close(self, a, b):
        ax, ay = (
            (a.rect.centerx, a.rect.centery)
            if hasattr(a, "rect")
            else (a.position.x, a.position.y)
        )
        bx, by = (
            (b.rect.centerx, b.rect.centery)
            if hasattr(b, "rect")
            else (b.position.x, b.position.y)
        )
        dx = ax - bx
        dy = ay - by
        return (dx * dx + dy * dy) ** 0.5 <= self.INTERACTION_DISTANCE

    def _handle_interaction(self, student):
        student.target_pos = student.exit_pos
        student.state = "leaving"
        
        # Llamar al callback si existe
        if self.on_interaction:
            self.on_interaction()
