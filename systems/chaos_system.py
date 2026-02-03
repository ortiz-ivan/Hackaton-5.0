# systems/chaos_system.py


class ChaosSystem:
    def __init__(self, config):
        self.max_chaos = config.MAX_CHAOS
        self.chaos = 0

        # freeze flag used by powerups
        self.frozen = False

        # Dificultad dinámica
        self.base_spawn_rate = config.BASE_SPAWN_RATE
        self.spawn_rate = self.base_spawn_rate

        self.speed_multiplier = 1.0
        self.obstacle_chance = 0.0

    # ─────────────────────────────
    # Eventos del juego
    # ─────────────────────────────

    def on_correct_interaction(self, student_state):
        """
        El jugador atendió correctamente a un alumno.
        """
        if student_state == "QUESTION":
            self.decrease_chaos(2)
        elif student_state == "TALK":
            self.decrease_chaos(3)
        elif student_state == "SLEEP":
            self.decrease_chaos(1)

    def on_failed_interaction(self):
        """
        Interacción incorrecta o interrumpida.
        """
        self.increase_chaos(5)

    def on_student_ignored(self):
        """
        Se agotó el timer de paciencia de un alumno.
        """
        self.increase_chaos(8)

    def freeze(self):
        """Temporarily pause chaos changes."""
        self.frozen = True

    def unfreeze(self):
        """Resume chaos changes."""
        self.frozen = False

    # ─────────────────────────────
    # Gestión interna del caos
    # ─────────────────────────────

    def increase_chaos(self, amount):
        if self.frozen:
            return
        self.chaos = min(self.max_chaos, self.chaos + amount)
        self._recalculate_difficulty()

    def decrease_chaos(self, amount):
        if self.frozen:
            return
        self.chaos = max(0, self.chaos - amount)
        self._recalculate_difficulty()

    def _recalculate_difficulty(self):
        """
        Ajusta parámetros globales según el caos actual.
        """
        chaos_ratio = self.chaos / self.max_chaos

        self.spawn_rate = self.base_spawn_rate * (1 + chaos_ratio)
        self.speed_multiplier = 1 + chaos_ratio * 0.5
        self.obstacle_chance = chaos_ratio

    # ─────────────────────────────
    # Consultas externas
    # ─────────────────────────────

    def is_game_over(self):
        return self.chaos >= self.max_chaos

    def get_spawn_rate(self):
        return self.spawn_rate

    def get_speed_multiplier(self):
        return self.speed_multiplier

    def get_obstacle_chance(self):
        return self.obstacle_chance

    def get_chaos(self):
        return self.chaos
