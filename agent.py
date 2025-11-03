import random
class Agent:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
        self.evacuated = False

    def move(self, pheromone_map, env):
        if self.evacuated:
            return
        directions = [0, 1, 2, 3]
        best_dir = self.direction
        max_score = -1
        for d in directions:
            dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][d]
            nx, ny = self.x + dx, self.y + dy
            if env.is_valid(nx, ny):
                p = pheromone_map[nx, ny]
                p += env.get_hospital_score(nx, ny) * 0.01
                p += env.get_shelter_score(nx, ny) * 0.01
                p -= env.get_transport_penalty(nx, ny) * 0.5
                if p > max_score:
                    max_score = p
                    best_dir = d
        self.direction = best_dir
        dx, dy = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.direction]
        nx, ny = self.x + dx, self.y + dy
        if env.is_exit(nx, ny):
            self.evacuated = True
        elif env.is_valid(nx, ny):
            self.x, self.y = nx, ny