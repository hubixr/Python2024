import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# Define symbols
t = sp.symbols('t')
x = sp.Function('x')(t)
m, k, c, F0, omega = sp.symbols('m k c F0 omega')

# Define the differential equations
damped_eq = sp.Eq(m * x.diff(t, t) + c * x.diff(t) + k * x, 0)
forced_eq = sp.Eq(m * x.diff(t, t) + c * x.diff(t) + k * x, F0 * sp.cos(omega * t))

# Solve the differential equations
damped_sol = sp.dsolve(damped_eq, x)
forced_sol = sp.dsolve(forced_eq, x)

# Print the solutions
print("Damped Harmonic Oscillator Solution:")
sp.pprint(damped_sol)
print("\nForced Harmonic Oscillator Solution:")
sp.pprint(forced_sol)

# Define parameters for plotting
m_val = 1
k_val = 1
c_vals = [0.1, 0.5, 1.0]
F0_val = 1
omega_vals = [0.5, 1.0, 2.0]
t_vals = np.linspace(0, 20, 400)

# Plot the solutions
for c_val in c_vals:
    damped_sol_func = sp.lambdify(t, damped_sol.rhs.subs({m: m_val, k: k_val, c: c_val}).evalf(), 'numpy')
    plt.plot(t_vals, damped_sol_func(t_vals), label=f'c={c_val}')
plt.title('Damped Harmonic Oscillator')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.show()

for omega_val in omega_vals:
    forced_sol_func = sp.lambdify(t, forced_sol.rhs.subs({m: m_val, k: k_val, c: c_vals[1], F0: F0_val, omega: omega_val}).evalf(), 'numpy')
    plt.plot(t_vals, forced_sol_func(t_vals), label=f'omega={omega_val}')
plt.title('Forced Harmonic Oscillator')
plt.xlabel('Time')
plt.ylabel('Displacement')
plt.legend()
plt.show()
