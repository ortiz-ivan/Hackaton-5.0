import pygame

# X: Centradas en las sillas azules
columnas_x = [127, 207, 350, 431, 571, 654]
# Y: Ajustadas a los "pasillos" blancos entre mesas
# Se han movido para que el rect.midbottom no toque las cajas de colisión (Obstacles)
filas_y = [135, 185, 230, 305, 350, 400, 480, 525, 570]

SEATS = []
for y in filas_y:
    for x in columnas_x:
        SEATS.append(pygame.Vector2(x, y))

assert len(SEATS) == 54