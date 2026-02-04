import os
import pygame


class PowerUpSystem:
    """Gestiona la aplicación de efectos de power-ups"""

    def __init__(self, player, students, chaos_system):
        self.player = player
        self.students = students
        self.chaos_system = chaos_system

        # Duración de efectos temporales (en segundos)
        # Claves posibles: "speed", "freeze", "slow"
        self.active_effects = {}

        # Sonido al recoger powerup
        self.pickup_sound = self._load_pickup_sound()

        # Flash de pantalla al recoger (en segundos)
        self.flash_duration = 0.15
        self.flash_timer = 0.0

    def _load_pickup_sound(self):
        """Carga el sonido de recogida, si está disponible."""
        try:
            path = os.path.join(
                "assets", "sounds", "interact", "comic_chat_ interactive.mp3"
            )
            return pygame.mixer.Sound(path)
        except pygame.error:
            return None

    def check_collection(self, powerups):
        """Verifica si el jugador colisiona con algún power-up"""
        for powerup in powerups:
            if powerup.active and self.player.rect.colliderect(powerup.rect):
                self.apply_effect(powerup)
                powerup.active = False
                # Feedback de recogida
                if self.pickup_sound:
                    self.pickup_sound.play()
                self.flash_timer = self.flash_duration

    def apply_effect(self, powerup):
        """Aplica el efecto del power-up según su tipo"""

        if powerup.type == "speed":
            # Aumenta MUCHO la velocidad del jugador temporalmente
            if not hasattr(self.player, "base_speed"):
                self.player.base_speed = self.player.speed
            self.player.speed = self.player.base_speed * 2.0
            self.active_effects["speed"] = 6.0

        elif powerup.type == "attention":
            # Resetea a estado neutral a estudiantes que necesitan atención (talking/question)
            for student in self.students:
                if (
                    student.state == "waiting"
                    and getattr(student, "icon", None) in ["talking", "question"]
                ):
                    student.reset_state()

        elif powerup.type == "patience":
            # Aumenta el tiempo de paciencia de todos los estudiantes esperando
            for student in self.students:
                if student.state == "waiting":
                    student.patience_timer += 5.0

        elif powerup.type == "freeze":
            # Congela a todos los estudiantes
            self.active_effects["freeze"] = 3.0
            for student in self.students:
                student.freeze()

        elif powerup.type == "calm":
            # Baja el caos global de golpe
            if self.chaos_system is not None:
                self.chaos_system.decrease_chaos(20)

        elif powerup.type == "slow":
            # Ralentiza a todos los estudiantes temporalmente
            self.active_effects["slow"] = 5.0
            for student in self.students:
                if not hasattr(student, "base_speed"):
                    student.base_speed = student.speed
                student.speed = student.base_speed * 0.5

    def update(self, powerups=None, dt=1 / 60):
        """Actualiza los efectos activos"""

        # Verificar colisión con power-ups
        if powerups:
            self.check_collection(powerups)

        # Actualizar timers de efectos temporales
        expired_effects = []
        for effect in list(self.active_effects.keys()):
            self.active_effects[effect] -= dt

            if self.active_effects[effect] <= 0:
                expired_effects.append(effect)

        # Remover efectos expirados
        for effect in expired_effects:
            self.remove_effect(effect)
            del self.active_effects[effect]

        # Actualizar flash de pantalla
        if self.flash_timer > 0:
            self.flash_timer -= dt
            if self.flash_timer < 0:
                self.flash_timer = 0

    def remove_effect(self, effect):
        """Remueve un efecto cuando expira"""
        if effect == "speed":
            if hasattr(self.player, "base_speed"):
                self.player.speed = self.player.base_speed

        elif effect == "freeze":
            # Descongelar TODOS los estudiantes
            for student in self.students:
                student.unfreeze()

        elif effect == "slow":
            # Restaurar velocidad original de los estudiantes
            for student in self.students:
                if hasattr(student, "base_speed"):
                    student.speed = student.base_speed