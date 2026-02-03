from entities.student import Student
import random


class SpawnSystem:
    def __init__(self):
        self.spawned = False
        self.initial_position = (720, 500)  # posición donde aparecen los NPCs
        self.timer = 0
        self.spawn_interval = 5  # segundos

    def spawn_initial(self, students, get_free_seat, exit_position):
        """
        Crea los estudiantes iniciales y los asigna a asientos.
        get_free_seat: función que retorna un asiento libre (Vector2) y su índice
        exit_position: Vector2 de la salida
        """
        if self.spawned:
            return

        for _ in range(5):  # spawn inicial de 5 estudiantes
            result = get_free_seat()
            if result is None:
                continue
            seat_pos, seat_index = result

            student = Student(
                spawn_pos=self.initial_position,
                seat_pos=seat_pos,
                exit_pos=exit_position,
                seat_index=seat_index,
            )
            students.append(student)

        self.spawned = True

    def update(self, dt, students, get_free_seat, exit_position):
        """
        Spawn dinámico cada spawn_interval segundos si hay asientos libres.
        """
        self.timer += dt
        if self.timer >= self.spawn_interval:
            result = get_free_seat()
            if result is not None:
                seat_pos, seat_index = result
                student = Student(
                    spawn_pos=self.initial_position,
                    seat_pos=seat_pos,
                    exit_pos=exit_position,
                    seat_index=seat_index,
                )
                students.append(student)
            self.timer = 0
