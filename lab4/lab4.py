import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from rich.progress import track
import os
from numba import jit
import time

def initialize_model(grid_size, J, beta, B, steps, spin_density=0.5, filename_prefix=None, filename_animation=None, filename_magnetization=None, outputfolder=None):
    model = {
        'grid_size': grid_size,
        'J': J,
        'beta': beta,
        'B': B,
        'steps': steps,
        'spin_density': spin_density,
        'filename_prefix': filename_prefix,
        'filename_animation': filename_animation,
        'filename_magnetization': filename_magnetization,
        'outputfolder': outputfolder,
        'grid': np.random.choice([-1, 1], size=(grid_size, grid_size), p=[1 - spin_density, spin_density]),
        'magnetization': [],
        'frames': []
    }
    os.makedirs(outputfolder, exist_ok=True)
    return model

@jit(nopython=True)
def calculate_energy(grid, J, B, x, y, grid_size):
    neighbors = [((x - 1) % grid_size, y), ((x + 1) % grid_size, y), 
                 (x, (y - 1) % grid_size), (x, (y + 1) % grid_size)]
    interaction_energy = - J * grid[x, y] * (
        grid[neighbors[0][0], neighbors[0][1]] + grid[neighbors[1][0], neighbors[1][1]] +
        grid[neighbors[2][0], neighbors[2][1]] + grid[neighbors[3][0], neighbors[3][1]])
    field_energy = -B * grid[x, y]
    return interaction_energy + field_energy

@jit(nopython=True)
def step(grid, J, beta, B, grid_size):
    for _ in range(grid_size ** 2):
        x, y = np.random.randint(0, grid_size, size=2)
        dE = -2 * calculate_energy(grid, J, B, x, y, grid_size)

        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            grid[x, y] *= -1

def run(model, use_numba=True):
    start_time = time.time()
    for step_num in track(range(model['steps']), description="Simulating", transient=True):
        if use_numba:
            step(model['grid'], model['J'], model['beta'], model['B'], model['grid_size'])
        else:
            step_no_numba(model['grid'], model['J'], model['beta'], model['B'], model['grid_size'])
        magnetization = np.mean(model['grid'])
        model['magnetization'].append(magnetization)

        if model['filename_prefix']:
            save_image(model, step_num)

        if model['filename_animation']:
            model['frames'].append(model['grid'].copy())
    
    if model['filename_magnetization']:
        save_magnetization(model)

    if model['filename_animation']:
        save_animation(model)
    end_time = time.time()
    return end_time - start_time

def step_no_numba(grid, J, beta, B, grid_size):
    for _ in range(grid_size ** 2):
        x, y = np.random.randint(0, grid_size, size=2)
        dE = -2 * calculate_energy_no_numba(grid, J, B, x, y, grid_size)

        if dE < 0 or np.random.rand() < np.exp(-beta * dE):
            grid[x, y] *= -1

def calculate_energy_no_numba(grid, J, B, x, y, grid_size):
    neighbors = [((x - 1) % grid_size, y), ((x + 1) % grid_size, y), 
                 (x, (y - 1) % grid_size), (x, (y + 1) % grid_size)]
    interaction_energy = - J * grid[x, y] * (
        grid[neighbors[0][0], neighbors[0][1]] + grid[neighbors[1][0], neighbors[1][1]] +
        grid[neighbors[2][0], neighbors[2][1]] + grid[neighbors[3][0], neighbors[3][1]])
    field_energy = -B * grid[x, y]
    return interaction_energy + field_energy

def save_image(model, step):
    file_path = os.path.join(model['outputfolder'], model['filename_prefix'])
    plt.imshow(model['grid'], cmap="coolwarm")
    plt.title(f"Step {step}")
    plt.savefig(f"{file_path}_{step}.png")
    plt.close()

def save_magnetization(model):
    file_path = os.path.join(model['outputfolder'], model['filename_magnetization'])
    print("ścieżka", file_path)
    np.savetxt(file_path, model['magnetization'])

def save_animation(model):
    print("Saving animation")
    fig, ax = plt.subplots()
    def update(frame):
        ax.clear()
        ax.imshow(frame, cmap='coolwarm')

    anim = FuncAnimation(fig, update, frames=model['frames'], interval=100)
    anim.save(os.path.join(model['outputfolder'], model['filename_animation']), writer='imagemagick')
    plt.close()

# Example usage
if __name__ == "__main__":
    model = initialize_model(
        grid_size=64,
        J=1.0,
        beta=0.9,
        B=0.1,
        steps=100,
        filename_prefix="ising_step",
        filename_animation="ising_animation.gif",
        filename_magnetization="magnetization.txt",
        outputfolder="results_numba"
    )
    time_with_numba = run(model, use_numba=True)
    print(f"Simulation time with Numba: {time_with_numba} seconds")

    model = initialize_model(
        grid_size=64,
        J=1.0,
        beta=0.9,
        B=0.1,
        steps=100,
        filename_prefix="ising_step",
        filename_animation="ising_animation.gif",
        filename_magnetization="magnetization.txt",
        outputfolder="results_no_numba"
    )
    time_without_numba = run(model, use_numba=False)
    print(f"Simulation time without Numba: {time_without_numba} seconds")
    print(f"Simulation time difference: {time_without_numba-time_with_numba} seconds")