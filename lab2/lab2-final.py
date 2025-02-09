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
        self.grid = np.random.choice([-1,1], size=(grid_size, grid_size), p=[1 - spin_density, spin_density]) #losowane elementy 1 lub -1 , p=prawdopodobieństwo -1 wynosi 1-spin_density, a 1 wynosi spindensity
        self.magnetization = []
        self.frames = []
        os.makedirs(self.outputfolder, exist_ok=True)
        
    def calculate_energy(self, x, y):
        neighbors = [((x - 1) % self.grid_size, y), ((x + 1) % self.grid_size, y), 
                     (x, (y - 1) % self.grid_size), (x, (y + 1) % self.grid_size)]  # % operacja modulo, jeżeli wyjdzie poza siatke to przerzuca na drugą stronę i leci dalej
        interaction_energy = - self.J * self.grid[x,y] * (
            self.grid[neighbors[0][0], neighbors[0][1]] + self.grid[neighbors[1][0], neighbors[1][1]] +
            self.grid[neighbors[2][0], neighbors[2][1]] + self.grid[neighbors[3][0], neighbors[3][1]]) #neighbors wartości x,x,y,y sąsiedzi
        field_energy = -self.B * self.grid[x, y]
        return interaction_energy + field_energy # to jest moja zmiana energii, jak jest ujemna to zostaje jak jest, jak dodatnia to spin robi spin z prawdopodobieństwem
    
    def step(self):
        #pojedynczy krok metody
        for _ in range(self.grid_size ** 2):
            x, y = np.random.randint(0, self.grid_size, size= 2) #x,y przydziela 2 losowe liczby z grid_size
            dE = -2 * self.calculate_energy(x, y)

            if dE < 0 or np.random.rand() < np.exp(-self.beta * dE):
                self.grid[x, y] *= -1

    def run(self):
        for step in track(range(self.steps), description="Simulating", transient=True):
            self.step()
            magnetization = np.mean(self.grid)
            self.magnetization.append(magnetization)

            if self.filename_prefix:
                self.save_image(step)

            if self.filename_animation:
                self.frames.append(self.grid.copy())
        
        if self.filename_magnetization:
            self.save_magnetization()

        if self.filename_animation:
            self.save_animation()

    def save_image(self, step):
        self.file_path = os.path.join(self.outputfolder, self.filename_prefix)
        plt.imshow(self.grid, cmap="coolwarm")
        plt.title(f"Step {step}")
        plt.savefig(f"{self.file_path}_{step}.png")
        plt.close()

    def save_magnetization(self):
        self.file_path = os.path.join(self.outputfolder, self.filename_magnetization)
        print("ścieżka", self.file_path)
        np.savetxt(self.file_path, self.magnetization)

    def save_animation(self):
        print("Saving animation")
        fig, ax = plt.subplots()
        def update(frame):
            ax.clear()
            ax.imshow(frame, cmap='coolwarm')

        anim = FuncAnimation(fig, update, frames=self.frames, interval=100)
        anim.save(os.path.join(self.outputfolder, self.filename_animation), writer='imagemagick')
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
        outputfolder = "results"
    )
    model.run()