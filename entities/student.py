import pygame
import os
import random
from config import STUDENT_SIZE

class Student(pygame.sprite.Sprite):
    def __init__(self, position, target_position):
        super().__init__()

        self.position = pygame.Vector2(position)
        self.target_position = pygame.Vector2(target_position)

        self.speed = 200
        self.state = "walking"
        self.icon = None

        # Cargar imágenes
        self.images = {
            "walking": pygame.image.load(
                os.path.join("assets", "images", "alumno(1).png")
            ).convert_alpha(),
            "sleeping": pygame.image.load(
                os.path.join("assets", "images", "icons", "Durmiendo.png")
            ).convert_alpha(),
            "talking": pygame.image.load(
                os.path.join("assets", "images", "icons", "hablando.png")
            ).convert_alpha(),
            "question": pygame.image.load(
                os.path.join("assets", "images", "icons", "pregunta.png")
            ).convert_alpha(),
        }

        for key in self.images:
            self.images[key] = pygame.transform.scale(
                self.images[key], STUDENT_SIZE
            )

        self.image = self.images["walking"]
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, obstacles):
        if self.state == "walking":
            direction = self.target_position - self.position

            if direction.length() > 0:
                direction = direction.normalize()
                new_position = self.position + direction * self.speed * dt
                self.rect.center = new_position
                if not any(self.rect.colliderect(obstacle.rect) for obstacle in obstacles):
                    self.position = new_position
                self.rect.center = self.position

            if self.position.distance_to(self.target_position) < 10:
                self.state = "seated"
                self.icon = random.choice(["sleeping", "talking", "question"])
        elif self.state == "leaving":
            direction = self.target_position - self.position

            if direction.length() > 0:
                direction = direction.normalize()
                new_position = self.position + direction * self.speed * dt
                self.rect.center = new_position
                if not any(self.rect.colliderect(obstacle.rect) for obstacle in obstacles):
                    self.position = new_position
                self.rect.center = self.position

            if self.position.distance_to(self.target_position) < 10:
                self.state = "left"
            

    def render(self, screen):
        screen.blit(self.image, self.rect)
        if self.state == "seated" and self.icon:
            # Dibujar burbuja
            bubble_rect = pygame.Rect(self.rect.left - 10, self.rect.top - 50, 60, 40)
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), bubble_rect, 2, border_radius=10)
            # Dibujar icono
            icon_image = self.images[self.icon]
            icon_rect = icon_image.get_rect(center=bubble_rect.center)
            screen.blit(icon_image, icon_rect)
