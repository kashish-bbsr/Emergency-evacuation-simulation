# simulation.py
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import numpy as np
import imageio
import pandas as pd
import random
from agent import Agent
from environment import Environment
from pheromone_map import PheromoneMap


class Simulation:
    def __init__(self, width=50, height=50, num_agents=50):
        self.env = Environment(width, height)
        self.pheromones = PheromoneMap(width, height)
        self.frames = []

        # Load CSV files (with error handling)
        try:
            self.env.load_shelters("data/Shelter_Data.csv")
            self.env.load_transport_hazards("data/Transport_Data.csv")
            self.env.load_hospitals("data/Hospital_Data.csv")
        except FileNotFoundError as e:
            print(f"Warning: CSV file not found: {e}. Using default positions.")

        # Seed pheromone at shelters so agents can smell them
        self.env.seed_shelter_pheromones(self.pheromones, base_amount=50.0)

        # Create agents at random valid positions
        self.agents = []
        for _ in range(num_agents):
            while True:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)
                if self.env.is_valid(x, y) and not self.env.is_exit(x, y):
                    break
            self.agents.append(Agent(x, y, random.randint(0, 3)))

    def step(self):
        # Move agents and deposit pheromone
        for agent in self.agents:
            if not agent.evacuated:
                agent.move(self.pheromones.map, self.env)
                if not agent.evacuated:
                    self.pheromones.deposit(agent.x, agent.y, amount=1.0)
        # Diffuse and decay pheromone
        self.pheromones.diffuse_and_decay(self.env)

    def visualize(self):
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.imshow(self.pheromones.map.T, cmap='hot', origin='lower', alpha=0.7)

        # Plot active agents
        active_count = 0
        for agent in self.agents:
            if not agent.evacuated:
                ax.plot(agent.x, agent.y, 'bo', markersize=4)
                active_count += 1

        # Plot static features
        for points, color, marker, label in [
            (self.env.exits, 'lime', 's', 'Shelter'),
            (self.env.hospitals, 'cyan', '^', 'Hospital'),
            (self.env.hazards, 'red', 'x', 'Hazard')
        ]:
            if points:
                xs, ys = zip(*points)
                ax.scatter(xs, ys, c=color, marker=marker, s=60, label=label, edgecolors='black', linewidth=0.5)

        # Title and info
        ax.set_title("Emergency Evacuation Simulation", fontsize=14, fontweight='bold')
        ax.text(1, 1, f"Step: {len(self.frames)} | Active: {active_count}",
                color='white', fontsize=10, bbox=dict(facecolor='black', alpha=0.6))

        # Legend
        handles, labels = ax.get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), loc='upper right', fontsize=8)

        # Save frame
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.buffer_rgba(), dtype=np.uint8)
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (4,))[:, :, :3]
        self.frames.append(image)
        plt.close(fig)

    def run(self, steps=120):
        print("Starting simulation...")
        evacuated_over_time = []

        for step_num in range(steps):
            self.step()
            self.visualize()

            # Track evacuation
            evacuated = sum(1 for a in self.agents if a.evacuated)
            evacuated_over_time.append(evacuated)

            if step_num % 20 == 0:
                print(f"Step {step_num}: {evacuated} evacuated")

        # Final report
        total_evacuated = sum(1 for a in self.agents if a.evacuated)
        print(f"\nFINAL: {total_evacuated}/{len(self.agents)} evacuated "
              f"({100 * total_evacuated / len(self.agents):.1f}%)")

        # Plot evacuation curve
        plt.figure(figsize=(8, 4))
        plt.plot(evacuated_over_time, 'g-', linewidth=2)
        plt.title("Evacuation Progress Over Time")
        plt.xlabel("Simulation Step")
        plt.ylabel("Agents Evacuated")
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig("evacuation_curve.png", dpi=150)
        plt.close()
        print("Graph saved: evacuation_curve.png")

        # Save video
        self.save_video("evacuation.mp4")

    def save_video(self, filename="evacuation.mp4"):
        if not self.frames:
            print("No frames to save!")
            return
        imageio.mimsave(filename, self.frames, fps=20, codec='libx264')
        print(f"SAVED: {filename} ({len(self.frames)} frames)")