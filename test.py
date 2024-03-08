import matplotlib.pyplot as plt
import numpy as np

# Definir las variables
velocidad_inicial = 10 # m/s
angulo_disparo = 45 # grados
altura_inicial = 0 # m

# Convertir el ángulo a radianes
angulo_disparo = angulo_disparo * np.pi / 180

# Calcular el tiempo de vuelo
tiempo_vuelo = 2 * velocidad_inicial * np.sin(angulo_disparo) / 9.81

# Definir los vectores de tiempo, posición y velocidad
# Definir los vectores de tiempo, posición y velocidad
t = np.linspace(0, tiempo_vuelo, 100)
x = velocidad_inicial * t * np.cos(angulo_disparo)
y = altura_inicial + velocidad_inicial * t * np.sin(angulo_disparo) - 0.5 * 9.81 * t**2

# Calcular el valor máximo de x
x_max = np.max(x)

# Crear la figura y el eje
fig, ax = plt.subplots()

# Establecer los límites del eje x
ax.set_xlim((0, x_max))
ax.set_ylim((0, np.max(y)))

# Crear un objeto Line2D vacío
line, = ax.plot([], [], color="red", marker="o")

# Bucle para la animación
for i in range(len(t)):
    # Actualizar los datos del objeto Line2D
    line.set_data(x[i], y[i])

    # Agregar etiquetas a los ejes
    ax.set_xlabel("Distancia horizontal (m)")
    ax.set_ylabel("Altura (m)")

    # Mostrar la figura
    plt.pause(0.01)

# Mostrar la figura final
plt.show()