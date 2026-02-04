import pygame
import os
import random
from config import STUDENT_SIZE


class Student(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, seat_pos, exit_pos, seat_index=None, get_free_seat=None):
        super().__init__()

        # Posiciones
        self.position = pygame.Vector2(seat_pos)  # Aparece directamente en la silla
        self.seat_pos = pygame.Vector2(seat_pos)
        self.exit_pos = pygame.Vector2(exit_pos)
        self.target_pos = self.seat_pos  # inicial, va al asiento
        self.seat_index = seat_index  # índice del asiento para liberar

        # Movimiento
        self.speed = 200
        self.move_direction = pygame.Vector2(0, 0)

        # Estado inicial
        self.state = "waiting"  # Ya sentado, no camina
        self.icon = None

        self.get_free_seat = get_free_seat  # función para obtener asiento libre

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

    def update(self, dt, obstacles, students, get_free_seat):

        # --- LÓGICA DE SALIDA POR PASILLOS ---
        if self.state == "leaving":
            # 1. Definimos el punto del pasillo central (X=710 es el pasillo de la derecha)
            # Primero se mueve hacia la derecha para salir de entre las mesas
            if abs(self.position.x - 710) > 10:
                target_x = 710
                target_y = self.position.y # Mantiene su altura actual
            else:
                # 2. Una vez en el pasillo derecho, baja hacia la puerta
                target_x = 710
                target_y = self.exit_pos.y

            target = pygame.Vector2(target_x, target_y)
            direction = target - self.position
            
            if direction.length() > 5:
                direction = direction.normalize()
                self.position += direction * self.speed * dt
                self.rect.midbottom = self.position
            else:
                if target_y == self.exit_pos.y: # Si ya llegó a la puerta final
                    self.state = "left"
            return
        # Solo moverse si está caminando o dejando
        if self.state in ["walking_to_seat", "leaving"]:
            direction = self.target_pos - self.position
            if direction.length() > 0:
                direction = direction.normalize()
                self.move_direction = direction
            else:
                self.move_direction = pygame.Vector2(0, 0)

            # Verificar si llegó al target
            if self.position.distance_to(self.target_pos) < 60:
                if self.state == "walking_to_seat":
                    # Verificar si el asiento está ocupado por otro estudiante
                    occupied = any(
                        s != self and s.state in ["waiting", "walking_to_seat"] and
                        s.position.distance_to(self.target_pos) < 30
                        for s in students
                    )
                    if occupied:
                        # Buscar otro asiento libre
                        result = get_free_seat()
                        if result:
                            new_seat_pos, new_seat_index = result
                            self.target_pos = new_seat_pos
                            self.seat_index = new_seat_index
                            # Continuar moviéndose
                        else:
                            # No hay asientos libres, quedarse esperando o algo
                            pass
                    else:
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
