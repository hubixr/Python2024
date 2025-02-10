from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.layouts import column
import numpy as np
from scipy.integrate import odeint

#poetry run bokeh serve --show .\dashboard.py

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

# Czas symulacji w dniach
t = np.linspace(0, 360, 360) # 360 dni co 1 dzien

def solve_sir(beta, gamma):
    solution = odeint(sir_model, initial_conditions, t, args=(beta, gamma))
    S, I, R = solution.T
    return S, I, R

beta = 0.3
gamma = 0.1
S, I, R = solve_sir(beta, gamma)

source = ColumnDataSource(data={'t': t, 'S': S, 'I': I, 'R': R})

#wykres
plot = figure(title='SIR Model', x_axis_label='Time (days)', y_axis_label='Proportion of Population', height=400, width=700)
plot.line('t', 'S', source=source, legend_label='Podatni', color='blue')
plot.line('t', 'I', source=source, legend_label='Zarażeni', color='red')
plot.line('t', 'R', source=source, legend_label='Martwi/Wyzdrowiali', color='green')
plot.legend.location = 'center_right'
plot.legend.click_policy = 'hide'

# Slidery
beta_slider = Slider(start=0.1, end=1.0, value=beta, step=0.01, title='Beta')
gamma_slider = Slider(start=0.05, end=0.5, value=gamma, step=0.01, title='Gamma')


def update(attr, old, new):
    beta = beta_slider.value
    gamma = gamma_slider.value
    S, I, R = solve_sir(beta, gamma)
    source.data = {'t': t, 'S': S, 'I': I, 'R': R}

beta_slider.on_change('value', update)
gamma_slider.on_change('value', update)


layout = column(beta_slider, gamma_slider, plot)
curdoc().add_root(layout)
curdoc().title = 'SIR Model Dashboard'
