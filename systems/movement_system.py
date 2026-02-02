class MovementSystem:
    def __init__(self, player, obstacles, input_system):
        self.player = player
        self.obstacles = obstacles
        self.input_system = input_system

    def update(self, dt, students):
        # Update player position
        direction = self.input_system.direction
        self.player.update(dt, direction)

        # Update students if needed
        for student in students:
            student.update(dt)

        # Update obstacles
        for obstacle in self.obstacles:
            obstacle.update()
            
            