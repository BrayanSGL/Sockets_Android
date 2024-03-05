import numpy as np
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Definir la función parabólica
def parabola(x):
    return 10 * (x/100) * (1 - x/100)

# Crear la figura y los ejes
fig, ax = plt.subplots()

# Crear el punto rojo
point, = ax.plot(0, 0, 'ro')

# Configurar los límites de los ejes
ax.set_xlim(0, 100)
ax.set_ylim(0, 10)

# Dibujar el cañón
cannon, = ax.plot([0, 10], [0, 1], 'k-')

# Función de inicialización para la animación
def init():
    point.set_data(0, 0)
    cannon.set_data([0, 10], [0, 1])
    return point, cannon,

# Función de animación
def animate(i):
    x = i
    y = parabola(i)
    point.set_data(x, y)
    return point, cannon,

# Número de cuadros
num_frames = 300

# Crear la animación
ani = animation.FuncAnimation(fig, animate, frames=np.linspace(0, 100, num_frames), init_func=init, blit=True, interval=1000/num_frames, repeat=True)

# Crear la ventana de tkinter
root = tk.Tk()

# Crear el canvas de tkinter y añadirlo a la ventana
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1) 

# Iniciar el bucle de eventos de tkinter
root.mainloop()