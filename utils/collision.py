import pygame

def check_collision(rect1, rect2, offset_x=0, offset_y=0):
    #Verifica si dos rectángulos colisionan, permitiendo reducir 
    #el área de impacto para que se sienta más natural.
    # Creamos una versión encogida del rect1 para la colisión
    collision_rect = rect1.inflate(-offset_x, -offset_y)
    
    return collision_rect.colliderect(rect2)

def get_future_rect(current_rect, velocity):
    #Calcula dónde estaría el rectángulo en el siguiente frame.
    #Útil para la 'Validación' antes de mover al profesor.
    future_rect = current_rect.copy()
    future_rect.x += velocity[0]
    future_rect.y += velocity[1]
    return future_rect