from entities.student import Student
import random

class SpawnSystem:
    def __init__(self):
        self.spawned = False
        self.initial_position = (400, 50)
        self.spawn_positions = [
            (400, 300),
            (550, 300),
        ]
        self.timer = 0
        self.spawn_interval = 5  # segundos

    def spawn_initial(self, students):
        if self.spawned:
            return

        for target in self.spawn_positions:
            student = Student(self.initial_position, target)
            students.append(student)

        self.spawned = True

    def update(self, dt, students):
        self.timer += dt
        if self.timer >= self.spawn_interval:
            target = random.choice(self.spawn_positions)
            student = Student(self.initial_position, target)
            students.append(student)
            self.timer = 0
