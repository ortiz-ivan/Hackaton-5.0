class GameClock:
    def __init__(self):
        self.elapsed_time = 0.0

        self.base_spawn_interval = 3.0
        self.min_spawn_interval = 0.8

        self.base_chaos_multiplier = 1.0
        self.max_chaos_multiplier = 3.0

    def update(self, dt: float):
        self.elapsed_time += dt

    @property
    def difficulty(self) -> float:
        return 1.0 + (self.elapsed_time / 60.0)

    @property
    def spawn_interval(self) -> float:
        interval = self.base_spawn_interval / self.difficulty
        return max(self.base_spawn_interval, interval)

    @property
    def chaos_multiplier(self) -> float:
        value = self.base_chaos_multiplier * self.difficulty
        return min(self.max_chaos_multiplier, value)
