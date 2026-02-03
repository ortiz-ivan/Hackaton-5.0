# systems/interaction_system.py


class InteractionSystem:
    INTERACTION_DISTANCE = 40  # píxeles

    def __init__(self, player, chaos_system, input_system):
        self.player = player
        self.chaos_system = chaos_system
        self.input_system = input_system

    def update(self, students):
        # Solo actuamos si el jugador intenta interactuar
        if not self.input_system.interact_pressed:
            return

        student = self._get_nearby_student(students)

        if student is None:
            # Interacción al aire → error
            self.chaos_system.on_failed_interaction()
            return

        self._handle_interaction(student)

    def _get_nearby_student(self, students):
        for student in students:
            if self._is_close(self.player, student):
                return student
        return None

    def _is_close(self, a, b):
        dx = a.rect.centerx - b.rect.centerx
        dy = a.rect.centery - b.rect.centery
        return (dx * dx + dy * dy) ** 0.5 <= self.INTERACTION_DISTANCE

    def _handle_interaction(self, student):
        if student.can_interact():
            student.on_interact_success()
            self.chaos_system.on_correct_interaction(student.state)
            self.player.add_prestige(student.get_prestige_reward())
        else:
            student.on_interact_fail()
            self.chaos_system.on_failed_interaction()
