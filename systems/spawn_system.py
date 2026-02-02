import pygame
import random
from entities.student import Student
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class SpawnSystem:
    def __init__(self):
        self.spawned = False
    
    def update(self, dt, spawn_interval, students):
        if not self.spawned:
            # Spawn two students at fixed positions (chairs)
            chair_positions = [(200, 400), (500, 400)]  # Adjust based on aula.png
            images = ['alumno(1).png', 'alumno(2).png']
            for i, pos in enumerate(chair_positions):
                student = Student(pos, images[i % len(images)])
                students.append(student)
            self.spawned = True 

