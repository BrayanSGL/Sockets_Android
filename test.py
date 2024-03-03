import tkinter as tk

def on_button_click():
    canvas.create_rectangle(10, 10, 50, 50, fill="blue")

# Crear la ventana principal
root = tk.Tk()
root.title("Interfaz con Botones y Canvas")

# Crear un Frame para los botones
button_frame = tk.Frame(root, width=100, height=300, bg="gray")
button_frame.pack(side=tk.LEFT, fill=tk.Y)

# Crear un botón en el Frame de los botones
button = tk.Button(button_frame, text="Dibujar Rectángulo", command=on_button_click)
button.pack(pady=10)

# Crear un Frame para el Canvas
canvas_frame = tk.Frame(root, width=400, height=300)
canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Crear un Canvas en el Frame del Canvas
canvas = tk.Canvas(canvas_frame, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Iniciar el bucle principal
root.mainloop()
