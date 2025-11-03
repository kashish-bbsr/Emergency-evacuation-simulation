import numpy as np
import pandas as pd

class Environment:
    def __init__(self, width, height):
        self.grid = np.zeros((width, height))
        self.exits = []
        self.hazards = []
        self.hospitals = []
        self.density_map = np.zeros((width, height))
        self.hospital_scores = {}
        self.shelter_scores = {}
        self.transport_penalty = {}

    def is_valid(self, x, y):
        return 0 <= x < self.grid.shape[0] and 0 <= y < self.grid.shape[1] and (x, y) not in self.hazards

    def is_exit(self, x, y):
        return (x, y) in self.exits

    def is_hospital(self, x, y):
        return (x, y) in self.hospitals

    def get_density(self, x, y):
        return self.density_map[x, y] if 0 <= x < self.grid.shape[0] and 0 <= y < self.grid.shape[1] else 0

    def get_hospital_score(self, x, y):
        return self.hospital_scores.get((x, y), 0)

    def get_shelter_score(self, x, y):
        return self.shelter_scores.get((x, y), 0)

    def get_transport_penalty(self, x, y):
        return self.transport_penalty.get((x, y), 0)

    def load_hospitals(self, csv_path):
        df = pd.read_csv(csv_path)
        for i, row in df.iterrows():
            x, y = 5 + i * 5, 5 + i * 5
            self.hospitals.append((x, y))
            score = row['ICU_Beds_Available'] + row['Ventilators_Available'] + row['Staff_On_Duty'] + row['Oxygen_Cylinders_Available']
            self.hospital_scores[(x, y)] = score

    def load_shelters(self, csv_path):
        df = pd.read_csv(csv_path)
        for i, row in df.iterrows():
            x, y = 10 + i * 3, 40 - i * 3
            self.exits.append((x, y))
            score = row['Utility_Score']
            self.shelter_scores[(x, y)] = score

    def load_transport_hazards(self, csv_path):
        df = pd.read_csv(csv_path)
        for i, row in df.iterrows():
            x, y = 25 + i * 2, 25 + i * 2
            penalty = 1 if row['Road_Condition'].lower() == 'poor' else 0
            self.hazards.append((x, y))
            self.transport_penalty[(x, y)] = penalty

    def load_density_map(self, csv_path):
        df = pd.read_csv(csv_path)
        for i, row in df.iterrows():
            x, y = 15 + i * 2, 15 + i * 2
            density = row.get('Wheat_kg', 0) + row.get('Rice_kg', 0)
            self.density_map[x, y] = density / 1000.0

    def seed_shelter_pheromones(self, pheromone_map, base_amount=50.0):
     for x, y in self.exits:
        if 0 <= x < pheromone_map.map.shape[0] and 0 <= y < pheromone_map.map.shape[1]:
            pheromone_map.deposit(x, y, base_amount)        