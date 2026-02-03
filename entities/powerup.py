import pygame

class PowerUp:
    """Representa un power-up individual en el juego"""
    
    TYPES = ["speed", "attention", "patience", "freeze"]
    
    COLOR_MAP = {
        "speed": (255, 100, 100),      # Rojo, aumenta velocidad
        "attention": (100, 255, 100),   # Verde, resetea estados
        "patience": (100, 100, 255),    # Azul, aumenta paciencia
        "freeze": (200, 200, 255)       # Azul claro, congela estudiantes
    }
    
    SIZE = 32
    
    def __init__(self, type, position):
        self.type = type
        self.position = pygame.Vector2(position)
        self.rect = pygame.Rect(position[0], position[1], self.SIZE, self.SIZE)
        self.active = True
        
        # Efecto visual (opcional: animación de pulso)
        self.pulse_timer = 0
        self.pulse_speed = 3.0
    
    def update(self, dt):
        """Actualiza la animación del power-up"""
        if self.active:
            self.pulse_timer += dt * self.pulse_speed
    
    def render(self, screen):
        """Dibuja el power-up con efecto de pulso"""
        if self.active:
            import math
            pulse = abs(math.sin(self.pulse_timer)) * 5
            size = self.SIZE + int(pulse)
            
            # Dibuja con el tamaño pulsante
            temp_rect = pygame.Rect(
                self.rect.centerx - size // 2,
                self.rect.centery - size // 2,
                size, size
            )
            pygame.draw.rect(screen, self.COLOR_MAP[self.type], temp_rect, border_radius=8)
            
            # Borde brillante
            pygame.draw.rect(screen, (255, 255, 255), temp_rect, 2, border_radius=8)