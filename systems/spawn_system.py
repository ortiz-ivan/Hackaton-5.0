import random
from entities.student import Student
from config import SCREEN_WIDTH, SCREEN_HEIGHT


class SpawnSystem:
    def __init__(self):
        self.timer = 0.0

        # Posiciones posibles (sillas del aula)
        self.spawn_positions = [
            (200, 400),
            (300, 400),
            (400, 400),
            (500, 400),
            (600, 400),
        ]

    def update(self, dt: float, spawn_interval: float, students: list):
        """
        Controla la aparición de nuevos alumnos.
        - dt: delta time
        - spawn_interval: tiempo entre spawns (definido por GameClock)
        - students: lista global de alumnos
        """
        self.timer += dt

        if self.timer >= spawn_interval:
            self.timer = 0.0
            self.spawn_student(students)

    def spawn_student(self, students: list):
        position = random.choice(self.spawn_positions)
        student = Student(position)
        students.append(student)
