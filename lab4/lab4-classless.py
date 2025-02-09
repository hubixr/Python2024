import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rich.progress import track
import os

class ModelIsinga():
    def __init__(self, grid_size, J, beta, B, steps, spin_density = 0.5, filename_prefix = None, filename_animation = None, filename_magnetization = None, outputfolder = None):
        self.grid_size = grid_size
        self.J = J
        self.beta = beta
        self.B = B
        self.steps = steps
        self.spin_density = spin_density
        self.filename_prefix = filename_prefix
        self.filename_animation = filename_animation
        self.filename_magnetization = filename_magnetization
        self.outputfolder = outputfolder

        #initialize spins with specified density
        self.grid = np.random.choice([-1,1], size=(grid_size, grid_size), p=[1 - spin_density, spin_density])
        self.magnetization = []
        self.frames = []
        os.makedirs(self.outputfolder, exist_ok=True)

def calculate_energy(model, x, y):
    neighbors = [((x - 1) % model.grid_size, y), ((x + 1) % model.grid_size, y), 
                 (x, (y - 1) % model.grid_size), (x, (y + 1) % model.grid_size)]
    interaction_energy = - model.J * model.grid[x,y] * (
        model.grid[neighbors[0][0], neighbors[0][1]] + model.grid[neighbors[1][0], neighbors[1][1]] +
        model.grid[neighbors[2][0], neighbors[2][1]] + model.grid[neighbors[3][0], neighbors[3][1]])
    field_energy = -model.B * model.grid[x, y]
    return interaction_energy + field_energy

def step(model):
    for _ in range(model.grid_size ** 2):
        x, y = np.random.randint(0, model.grid_size, size=2)
        dE = -2 * calculate_energy(model, x, y)

        if dE < 0 or np.random.rand() < np.exp(-model.beta * dE):
            model.grid[x, y] *= -1

def run(model):
    for step_num in track(range(model.steps), description="Simulating", transient=True):
        step(model)
        magnetization = np.mean(model.grid)
        model.magnetization.append(magnetization)

        if model.filename_prefix:
            save_image(model, step_num)

        if model.filename_animation:
            model.frames.append(model.grid.copy())
    
    if model.filename_magnetization:
        save_magnetization(model)

    if model.filename_animation:
        save_animation(model)

def save_image(model, step):
    file_path = os.path.join(model.outputfolder, model.filename_prefix)
    plt.imshow(model.grid, cmap="coolwarm")
    plt.title(f"Step {step}")
    plt.savefig(f"{file_path}_{step}.png")
    plt.close()

def save_magnetization(model):
    file_path = os.path.join(model.outputfolder, model.filename_magnetization)
    print("ścieżka", file_path)
    np.savetxt(file_path, model.magnetization)

def save_animation(model):
    print("Saving animation")
    fig, ax = plt.subplots()
    def update(frame):
        ax.clear()
        ax.imshow(frame, cmap='coolwarm')

    anim = FuncAnimation(fig, update, frames=model.frames, interval=100)
    anim.save(os.path.join(model.outputfolder, model.filename_animation), writer='imagemagick')
    plt.close()

# Example usage
if __name__ == "__main__":
    model = ModelIsinga(
        grid_size=128,
        J=1.0,
        beta=0.9,
        B=0.1,
        steps=100,
        filename_prefix="ising_step",
        filename_animation="ising_animation.gif",
        filename_magnetization="magnetization.txt",
        outputfolder="results"
    )
    run(model)