import pygame

class PowerUpSystem:
    """Gestiona la aplicación de efectos de power-ups"""
    
    def __init__(self, player, students, chaos_system):
        self.player = player
        self.students = students
        self.chaos_system = chaos_system
        
        # Duración de efectos temporales (en segundos)
        self.active_effects = {}
        
    def check_collection(self, powerups):
        """Verifica si el jugador colisiona con algún power-up"""
        for powerup in powerups:
            if powerup.active and self.player.rect.colliderect(powerup.rect):
                self.apply_effect(powerup)
                powerup.active = False
    
    def apply_effect(self, powerup):
        """Aplica el efecto del power-up según su tipo"""
        
        if powerup.type == "speed":
        # Aumenta velocidad temporalmente
            if not hasattr(self.player, 'base_speed'):
                self.player.base_speed = self.player.speed
            self.player.speed = self.player.base_speed + 100
            self.active_effects["speed"] = 5.0
            
        elif powerup.type == "attention":
            # Resetea a estado neutral a estudiantes que necesitan atención (talking/question)
            for student in self.students:
                if student.state == "waiting" and getattr(student, 'icon', None) in ["talking", "question"]:
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
                student.freeze()  # ← Usar método freeze()
        
    def update(self, powerups=None, dt=1/60):
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
    
    def remove_effect(self, effect):
        """Remueve un efecto cuando expira"""
        if effect == "speed":
            if hasattr(self.player, 'base_speed'):
                self.player.speed = self.player.base_speed
            
        elif effect == "freeze":
            # Descongelar TODOS los estudiantes
            for student in self.students:
                student.unfreeze()