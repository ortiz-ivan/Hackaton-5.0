from entities.student import Student

class SpawnSystem:
    def __init__(self):
        self.spawned = False
        self.initial_position = (400, 50)
        self.spawn_positions = [
            (400, 300),
            (550, 300),
        ]

    def spawn_initial(self, students):
        if self.spawned:
            return

        for target in self.spawn_positions:
            student = Student(self.initial_position, target)
            students.append(student)

        self.spawned = True
