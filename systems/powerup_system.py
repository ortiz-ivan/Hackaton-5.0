class PowerUpSystem:
    def __init__(self, player, students, chaos_system):
        self.player = player
        self.students = students
        self.chaos_system = chaos_system
        self.active_powerups = []

    def update(self, powerups):
        # Recolectar power-ups
        for pu in powerups:
            if pu.active and self.player.rect.colliderect(pu.rect):
                pu.activate()
                self.apply_powerup(pu)
                self.active_powerups.append(pu)

        # Revisar expiracion
        for pu in self.active_powerups[:]:
            if pu.is_expired():
                self.remove_powerup(pu)
                self.active_powerups.remove(pu)

    #definimos el metodo apply_powerup para aplicar el efecto del powerup
    def apply_powerup(self, pu):
        if pu.tipo == "speed":
            self.player.speed *= 2
        elif pu.tipo == "attention":
            self.player.interaction_time /= 2
        elif pu.tipo == "patience":
            for s in self.students:
                s.timer += 5
        elif pu.tipo == "freeze":
            self.chaos_system.freeze()
    
    #definimos el metodo remove_powerup para remover el efecto del powerup
    def remove_powerup(self, pu):
        if pu.tipo == "speed":
            self.player.speed /= 2
        elif pu.tipo == "attention":
            self.player.interaction_time *= 2
        elif pu.tipo == "patience":
            for s in self.students:
                s.timer -= 5
        elif pu.tipo == "freeze":
            self.chaos_system.unfreeze()
