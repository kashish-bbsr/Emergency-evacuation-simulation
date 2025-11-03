import numpy as np

class PheromoneMap:
    def __init__(self, width, height):
        self.map = np.zeros((width, height))

    def deposit(self, x, y, amount=1.0):
        self.map[x, y] += amount

    def diffuse_and_decay(self, env, decay=0.01, diffusion=0.1):
        new_map = self.map.copy()
        for x in range(1, self.map.shape[0] - 1):
            for y in range(1, self.map.shape[1] - 1):
                total = sum([self.map[x + dx, y + dy] for dx in [-1, 0, 1] for dy in [-1, 0, 1]])
                density_factor = 1 + env.get_density(x, y) * 0.05
                new_map[x, y] += diffusion * (total - 9 * self.map[x, y])
                new_map[x, y] *= (1 - decay * density_factor)
        self.map = new_map