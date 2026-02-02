import pygame

class InputSystem:
    def __init__(self, player):
        self.player = player
        self.direction = pygame.Vector2(0, 0)
        
    def update(self):
        keys = pygame.key.get_pressed()
        self.direction = pygame.Vector2(0, 0) 
        if keys [pygame.K_LEFT] or keys [pygame.K_a]:
            self.direction.x -=1
        if keys [pygame.K_RIGHT] or keys [pygame.K_d]:
            self.direction.x +=1
        if keys [pygame.K_UP] or keys [pygame.K_w]:
            self.direction.y -= 1
        if keys [pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y += 1
        if self.direction.length() > 0:
            self.direction.normalize()
            
    