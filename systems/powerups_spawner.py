import pygame
import random

class PowerUpSpawner:
    """Genera power-ups en posiciones aleatorias del mapa"""
    
    def __init__(self, player, students, obstacles):
        self.player = player
        self.students = students
        self.obstacles = obstacles
        
        # Configuración de spawn (intervalo se volverá ligeramente aleatorio)
        self.base_spawn_interval = 10.0  # valor medio en segundos
        self.spawn_interval = self._next_spawn_interval()
        self.spawn_timer = 0
        self.max_powerups = 3  # Máximo de power-ups simultáneos
        
        # Probabilidad de spawn por tipo
        self.spawn_weights = {
            "speed": 0.20,
            "attention": 0.25,
            "patience": 0.20,
            "freeze": 0.15,
            "calm": 0.10,
            "slow": 0.10,
        }

    def _next_spawn_interval(self):
        """Devuelve un nuevo intervalo de spawn ligeramente aleatorio."""
        # Entre 8 y 12 segundos para que no sea tan predecible
        return random.uniform(self.base_spawn_interval - 2, self.base_spawn_interval + 2)
    
    def get_random_position(self, screen_rect):
        """Genera una posición aleatoria válida para un power-up"""
        max_attempts = 50
        
        for _ in range(max_attempts):
            x = random.randint(50, screen_rect.width - 50)
            y = random.randint(50, screen_rect.height - 50)
            
            test_rect = pygame.Rect(x, y, 32, 32)
            
            # Verificar que no colisione con obstáculos
            collision = False
            for obstacle in self.obstacles:
                if test_rect.colliderect(obstacle.rect):
                    collision = True
                    break
            
            if collision:
                continue
            
            # Evitar spawn sobre el jugador
            if test_rect.colliderect(self.player.rect):
                continue
            
            # Evitar spawn sobre estudiantes
            for student in self.students:
                if test_rect.colliderect(student.rect):
                    collision = True
                    break
            if collision:
                continue
            
            return (x, y)
        
        # Si no encuentra posición, retorna centro de pantalla
        return (screen_rect.centerx, screen_rect.centery)
    
    def choose_powerup_type(self):
        """Selecciona un tipo de power-up según las probabilidades"""
        types = list(self.spawn_weights.keys())
        weights = list(self.spawn_weights.values())
        return random.choices(types, weights=weights)[0]
    
    def update(self, current_time, powerup_system, screen_rect):
        """Actualiza el spawner y genera nuevos power-ups si es necesario"""
        # Esta función debería recibir la lista de powerups activos
        # Por ahora asume que se maneja externamente
        pass
    
    def spawn(self, screen_rect):
        """Genera un nuevo power-up"""
        from entities.powerup import PowerUp
        
        position = self.get_random_position(screen_rect)
        powerup_type = self.choose_powerup_type()
        
        # Después de spawnear, recalculamos próximo intervalo
        self.spawn_interval = self._next_spawn_interval()

        return PowerUp(powerup_type, position)