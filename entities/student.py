import pygame
import os
import random
from config import STUDENT_SIZE


class Student(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, seat_pos, exit_pos, seat_index=None):
        super().__init__()

        # Posiciones
        self.position = pygame.Vector2(spawn_pos)
        self.seat_pos = pygame.Vector2(seat_pos)
        self.exit_pos = pygame.Vector2(exit_pos)
        self.target_pos = self.seat_pos  # inicial, va al asiento
        self.seat_index = seat_index  # índice del asiento para liberar

        # Movimiento
        self.speed = 200
        self.move_direction = pygame.Vector2(0, 0)

        # Estado inicial
        self.state = (
            "walking_to_seat"  # walking_to_seat, waiting, interacting, leaving, left
        )
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
            self.images[key] = pygame.transform.scale(self.images[key], STUDENT_SIZE)

        self.image = self.images["walking"]
        self.rect = self.image.get_rect(center=self.position)

    def update(self, dt, obstacles):
        # Solo moverse si está caminando o dejando
        if self.state in ["walking_to_seat", "leaving"]:
            direction = self.target_pos - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.move_direction = direction
                new_position = self.position + direction * self.speed * dt

                # Chequeo colisión con obstáculos
                self.rect.center = new_position
                if not any(self.rect.colliderect(ob.rect) for ob in obstacles):
                    self.position = new_position
                self.rect.center = self.position

            # Verificar si llegó al target
            if self.position.distance_to(self.target_pos) < 5:
                if self.state == "walking_to_seat":
                    self.state = "waiting"
                    self.move_direction = pygame.Vector2(0, 0)
                    self.icon = random.choice(["sleeping", "talking", "question"])
                elif self.state == "leaving":
                    self.state = "left"

    def on_interact_success(self):
        """El jugador interactuó correctamente: va a la salida"""
        self.target_pos = self.exit_pos
        self.state = "leaving"

    def on_interact_fail(self):
        """Interacción fallida: se queda esperando un poco más"""
        pass  # Podés agregar efecto de penalización de caos

    def can_interact(self):
        return self.state == "waiting"

    def render(self, screen):
        screen.blit(self.image, self.rect)

        # Dibujar ícono si está sentado
        if self.state == "waiting" and self.icon:
            bubble_rect = pygame.Rect(self.rect.left - 10, self.rect.top - 50, 60, 40)
            pygame.draw.rect(screen, (255, 255, 255), bubble_rect, border_radius=10)
            pygame.draw.rect(screen, (0, 0, 0), bubble_rect, 2, border_radius=10)
            icon_image = self.images[self.icon]
            icon_rect = icon_image.get_rect(center=bubble_rect.center)
            screen.blit(icon_image, icon_rect)
