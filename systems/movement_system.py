import pygame

class MovementSystem:
    def __init__(self, player, obstacles):
        self.player = player
        self.obstacles = obstacles

    def update(self, dt):
        direction = self.player.move_direction

        if direction.length_squared() == 0:
            return

        # 1. Calculamos el desplazamiento potencial total usando Delta Time
        displacement = direction * self.player.speed * dt
        
        # 2. Eje X: Intentamos mover y deslizar si hay colisión
        if direction.x != 0:
            new_pos_x = self.player.position.x + displacement.x
            # Creamos el rectángulo futuro solo para el eje X
            future_rect_x = pygame.Rect(new_pos_x, self.player.position.y, *self.player.size)
            
            if not self._check_collision(future_rect_x):
                self.player.position.x = new_pos_x

        # 3. Eje Y: Intentamos mover y deslizar si hay colisión
        if direction.y != 0:
            new_pos_y = self.player.position.y + displacement.y
            # Creamos el rectángulo futuro solo para el eje Y
            future_rect_y = pygame.Rect(self.player.position.x, new_pos_y, *self.player.size)
            
            if not self._check_collision(future_rect_y):
                self.player.position.y = new_pos_y

    def _check_collision(self, rect):
        #Valida si el rectángulo choca con algún obstáculo o límites.
        # Colisión con obstáculos (Sillas, mochilas, etc.) 
        for obstacle in self.obstacles:
            if rect.colliderect(obstacle.rect):
                return True
        
        # Opcional: Colisión con límites de la pantalla (Aula) [cite: 10]
        if rect.left < 0 or rect.right > 800: # Asumiendo 800 de ancho
            return True
        if rect.top < 0 or rect.bottom > 600: # Asumiendo 600 de alto
            return True
            
        return False
