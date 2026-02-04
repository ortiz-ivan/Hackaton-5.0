"""
Configuración de 72 sillas en el aula
Distribuidas en 9 filas x 8 columnas
"""

import pygame

# 72 coordenadas de sillas (9 filas x 8 columnas)
SEATS = [
    # Fila 1
    pygame.Vector2(200, 90),
    #pygame.Vector2(160, 50),
    #pygame.Vector2(240, 50),
    #pygame.Vector2(320, 50),
    #pygame.Vector2(400, 50),
    #pygame.Vector2(480, 50),
    #pygame.Vector2(560, 50),
    #pygame.Vector2(640, 50),
    #pygame.Vector2(720, 50),
    
    # Fila 2
    # pygame.Vector2(80, 110),
    # pygame.Vector2(160, 110),
    # pygame.Vector2(240, 110),
    # pygame.Vector2(320, 110),
    # pygame.Vector2(400, 110),
    # pygame.Vector2(480, 110),
    # pygame.Vector2(560, 110),
    # pygame.Vector2(640, 110),
    
    # Fila 3
    # pygame.Vector2(80, 170),
    # pygame.Vector2(160, 170),
    # pygame.Vector2(240, 170),
    # pygame.Vector2(320, 170),
    # pygame.Vector2(400, 170),
    # pygame.Vector2(480, 170),
    # pygame.Vector2(560, 170),
    # pygame.Vector2(640, 170),
    
    # Fila 4
    # pygame.Vector2(80, 230),
    # pygame.Vector2(160, 230),
    # pygame.Vector2(240, 230),
    # pygame.Vector2(320, 230),
    # pygame.Vector2(400, 230),
    # pygame.Vector2(480, 230),
    # pygame.Vector2(560, 230),
    # pygame.Vector2(640, 230),
    
    # Fila 5
    # pygame.Vector2(80, 290),
    # pygame.Vector2(160, 290),
    # pygame.Vector2(240, 290),
    # pygame.Vector2(320, 290),
    # pygame.Vector2(400, 290),
    # pygame.Vector2(480, 290),
    # pygame.Vector2(560, 290),
    # pygame.Vector2(640, 290),
    
    # Fila 6
    # pygame.Vector2(80, 350),
    # pygame.Vector2(160, 350),
    # pygame.Vector2(240, 350),
    # pygame.Vector2(320, 350),
    # pygame.Vector2(400, 350),
    # pygame.Vector2(480, 350),
    # pygame.Vector2(560, 350),
    # pygame.Vector2(640, 350),
    
    # Fila 7
    # pygame.Vector2(80, 410),
    # pygame.Vector2(160, 410),
    # pygame.Vector2(240, 410),
    # pygame.Vector2(320, 410),
    # pygame.Vector2(400, 410),
    # pygame.Vector2(480, 410),
    # pygame.Vector2(560, 410),
    # pygame.Vector2(640, 410),
    
    # Fila 8
    # pygame.Vector2(80, 470),
    # pygame.Vector2(160, 470),
    # pygame.Vector2(240, 470),
    # pygame.Vector2(320, 470),
    # pygame.Vector2(400, 470),
    # pygame.Vector2(480, 470),
    # pygame.Vector2(560, 470),
    # pygame.Vector2(640, 470),
    
    # Fila 9
    # pygame.Vector2(80, 530),
    # pygame.Vector2(160, 530),
    # pygame.Vector2(240, 530),
    # pygame.Vector2(320, 530),
    # pygame.Vector2(400, 530),
    # pygame.Vector2(480, 530),
    # pygame.Vector2(560, 530),
    # pygame.Vector2(640, 530),
]

assert len(SEATS) == 1, f"Se esperaban 9 sillas, pero hay {len(SEATS)}"
