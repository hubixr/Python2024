import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# S - susceptible, I - infected, R - removed
def sir_model(y, t, beta, gamma):
    S, I, R = y
    dS_dt = -beta * S * I
    dI_dt = beta * S * I - gamma * I
    dR_dt = gamma * I
    return [dS_dt, dI_dt, dR_dt]

# Warunki początkowe
S0 = 0.99
I0 = 0.01
R0 = 0.0
initial_conditions = [S0, I0, R0]

# parametry modelu
beta = 0.3  # współczynnik przenoszenia infekcji
gamma = 0.1  # współczynnik usuwania zainfekowanych

# Czas symulacji w dniach
t = np.linspace(0, 360, 360) # 360 dni co 1 dzien

# Rozwiązanie układu równań różniczkowych
solution = odeint(sir_model, initial_conditions, t, args=(beta, gamma))
S, I, R = solution.T

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(t, S, label='Podatni')
plt.plot(t, I, label='Zarażeni')
plt.plot(t, R, label='martwi/wyzdrowiali')
plt.xlabel('Time (days)')
plt.ylabel('Proportion of Population')
plt.title('SIR Model')
plt.legend()
plt.grid()
plt.show()
