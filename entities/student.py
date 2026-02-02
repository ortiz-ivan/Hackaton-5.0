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
        self.state_timer = 0
        self.state_duration = random.uniform(2, 5)

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

    def update(self, dt):
        if self.state == "walking":
            direction = self.target_position - self.position

            if direction.length() > 0:
                direction = direction.normalize()
                self.position += direction * self.speed * dt
                self.rect.center = self.position

            if self.position.distance_to(self.target_position) < 10:
                self._change_state()
        else:
            self.state_timer += dt
            if self.state_timer >= self.state_duration:
                self._change_state()

    def _change_state(self):
        self.state = random.choice(["sleeping", "talking", "question"])
        self.image = self.images[self.state]
        self.state_timer = 0
        self.state_duration = random.uniform(2, 5)

    def render(self, screen):
        screen.blit(self.image, self.rect)
