import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rich.progress import track
import os

class IsingModel:
    def __init__(self, grid_size, J, beta, B, steps, spin_density=0.5, 
                 image_prefix=None, animation_file=None, magnetization_file=None):
        self.grid_size = grid_size
        self.J = J
        self.beta = beta
        self.B = B
        self.steps = steps
        self.image_prefix = image_prefix
        self.animation_file = animation_file
        self.magnetization_file = magnetization_file

        # Initialize spins with given density
        self.grid = np.random.choice([-1, 1], size=(grid_size, grid_size), 
                                      p=[1 - spin_density, spin_density])
        self.magnetization = []
        self.frames = []  # For animation

    def calculate_energy(self, x, y):
        # Calculate local energy contribution for a spin
        neighbors = [(x - 1) % self.grid_size, (x + 1) % self.grid_size, 
                     (y - 1) % self.grid_size, (y + 1) % self.grid_size]
        interaction_energy = -self.J * self.grid[x, y] * (
            self.grid[neighbors[0], y] + self.grid[neighbors[1], y] +
            self.grid[x, neighbors[2]] + self.grid[x, neighbors[3]])
        field_energy = -self.B * self.grid[x, y]
        return interaction_energy + field_energy

    def step(self):
        # Perform a single Monte Carlo step
        for _ in range(self.grid_size ** 2):
            x, y = np.random.randint(0, self.grid_size, size=2)
            dE = -2 * self.calculate_energy(x, y)

            if dE < 0 or np.random.rand() < np.exp(-self.beta * dE):
                self.grid[x, y] *= -1

    def run(self):
        for step in track(range(self.steps), description="Simulating", transient=True):
            self.step()
            magnetization = np.mean(self.grid)
            self.magnetization.append(magnetization)

            if self.image_prefix:
                self.save_image(step)

            if self.animation_file:
                self.frames.append(self.grid.copy())

        if self.magnetization_file:
            self.save_magnetization()

        if self.animation_file:
            self.save_animation()

    def save_image(self, step):
        plt.imshow(self.grid, cmap='coolwarm')
        plt.title(f"Step {step}")
        plt.colorbar()
        plt.savefig(f"{self.image_prefix}_{step}.png")
        plt.close()

    def save_magnetization(self):
        np.savetxt(self.magnetization_file, self.magnetization)

    def save_animation(self):
        fig, ax = plt.subplots()
        def update(frame):
            ax.clear()
            ax.imshow(frame, cmap='coolwarm')

        anim = FuncAnimation(fig, update, frames=self.frames, interval=100)
        anim.save(self.animation_file, writer='imagemagick')
        plt.close()

# Example usage
if __name__ == "__main__":
    model = IsingModel(
        grid_size=50,
        J=1.0,
        beta=0.9,
        B=0.1,
        steps=10,
        image_prefix="ising_step",
        animation_file="ising_animation.gif",
        magnetization_file="magnetization.txt"
    )
    model.run()