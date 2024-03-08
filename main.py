import socket
import tkinter as tk
from tkinter import ttk
from threading import Thread
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as FuncAnimation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg #para combinar matplotlib con tkinter



BUFFER_SIZE = 2048
HOST = socket.gethostname()
SERVER_IP = socket.gethostbyname(HOST)
PORT = 6751

class Server:
    def __init__(self, host, port, gui) -> None:
        self.host = host
        self.port = port
        self.buffer_size = BUFFER_SIZE
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))
        self.server.listen(2)
        print(f"Esperando conexiones en {self.host}:{self.port} IP: {self.get_server_ip()}")
        self.clients = []
        self.gui = gui
        self.is_running = True

    def get_server_ip(self):
        return socket.gethostbyname(socket.gethostname())
    
    def accept_connections(self):
        while self.is_running:
            try:
                client, addr = self.server.accept()
                print(f"Conexión aceptada desde {addr[0]}:{addr[1]}")
                self.clients.append(client)
                self.gui.update_clients(self.clients)
                handle_client = Thread(target=self.handle_client, args=(client,))
                handle_client.start()  # Inicia el hilo
            except Exception as e:
                print(f"Error al aceptar conexiones: {e}")
                break

    def handle_client(self, client):
        try:
            client_address = client.getpeername()
            client.send("Bienvenido al servidor".encode("utf-8"))
            while self.is_running:
                data = client.recv(self.buffer_size)
                if not data:
                    break
                print(f"Mensaje de {client_address}: {data.decode('utf-8')}") # getpeername() devuelve la dirección del cliente
                for c in self.clients:
                    if c != client:
                        c.send(data)

                self.gui.root.after(0, self.gui.update_canvas(data.decode("utf-8"))) 

                if data.decode("utf-8") == "exit":
                    self.clients.remove(client)
                    client.close()
                    print(f"Conexión con {client_address} cerrada")
                    self.gui.update_clients(self.clients)
                    break
        except Exception as e:
            print(f"Error al manejar al cliente {client_address}: {e}")

    def close_server(self):
        print("Cerrando conexiones con clientes...")
        for client in self.clients:
            client.close()
        self.clients.clear()
        print("Cerrando servidor...")
        self.server.close()
        self.is_running = False
        print("Servidor cerrado")

class AppGUI:
    def __init__(self, root, server) -> None:
        self.root = root
        self.server = server
        self.root.title("Server")
        self.fig, self.ax = plt.subplots()
        self.canvas = None
        self.root.resizable(False, False)
        self.math_frame = None
        self.create_widgets()
        self.option = None

    def create_widgets(self):
        info_frame = tk.Frame(self.root, width=300, height=100)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        self.lbl_ip = ttk.Label(info_frame, text=f"IP: {self.server.get_server_ip()}")
        self.lbl_ip.pack()

        self.lbl_port = ttk.Label(info_frame, text=f"Puerto: {self.server.port}")
        self.lbl_port.pack()

        self.lbl_clients = ttk.Label(info_frame, text="Clientes conectados")
        self.lbl_clients.pack()

        self.list_clients = tk.Listbox(info_frame, width=30, height=10)
        self.list_clients.pack()

        self.btn_start = ttk.Button(info_frame, text="Iniciar servidor", command=self.start_server)
        self.btn_start.pack()

        self.btn_close = ttk.Button(info_frame, text="Cerrar servidor", command=self.close_server)
        self.btn_close.pack()

        self.math_frame = tk.Frame(self.root, width=300, height=200)
        self.math_frame.pack(side=tk.LEFT, fill=tk.BOTH)

        

    def start_server(self):
        print("Iniciando servidor")
        Thread(target=self.server.accept_connections).start() # Inicia el hilo para aceptar conexiones

    def close_server(self):
        print("Cerrando servidor")
        self.server.close_server()
        self.root.destroy()

    def update_clients(self, clients):
        self.list_clients.delete(0, tk.END) # Borra la lista
        for client in clients:
            self.list_clients.insert(tk.END, client.getpeername()) # Inserta la dirección del cliente



    def update_canvas(self, data):
        parts = data.split(":")
        operation = parts[0]
        print(data, type(data))
        self.option = operation

        if operation == "op_1":
            print("op_1")
            x = np.linspace(0, 2 * np.pi, 200) 
            y = float(parts[1]) * np.sin(float(parts[2]) * x)
            self.root.after(0, self.draw_plot(x, y))
            

        elif operation == "op_2":
            animation_thread = Thread(target=self.animate_bars)
            animation_thread.start()

        elif operation == "op_3":
            animation_thread = Thread(target=self.animate_lazamiento_parabolico)
            animation_thread.start()
        else:
            pass
        
    def draw_plot(self, x, y, color='b'):
        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.math_frame)
            self.canvas.get_tk_widget().pack()
        else:
            self.ax.clear()
        self.ax.plot(x, y, color)
        self.canvas.draw()

    def draw_bar(self, x, y):
        if self.canvas is None:
            self.canvas = FigureCanvasTkAgg(self.fig, master=self.math_frame)
            self.canvas.get_tk_widget().pack()
        else:
            self.ax.clear()
        self.ax.bar(x, y)
        self.ax.set_ylim([0, 100])  # Establece los límites del eje y
        self.canvas.draw()

    def animate_bars(self):
        x = [1, 2]
        y = [0, 100]
        for i in list(range(101)) + list(range(100, -1, -1)):
            if self.option != "op_2":
                break
            y[0] = i
            y[1] = 100 - i
            self.root.after(0, self.draw_bar(x, y))

    def animate_lazamiento_parabolico(self):
        
        velocidad_inicial = 10  # m/s
        angulo_disparo = 45  # grados
        altura_inicial = 0  # m

        # Convertir el ángulo a radianes
        angulo_disparo = angulo_disparo * np.pi / 180

        # Calcular el tiempo de vuelo
        tiempo_vuelo = 2 * velocidad_inicial * np.sin(angulo_disparo) / 9.81

        # Definir los vectores de tiempo, posición y velocidad
        t = np.linspace(0, tiempo_vuelo, 100)
        x = velocidad_inicial * t * np.cos(angulo_disparo)
        y = altura_inicial + velocidad_inicial * t * np.sin(angulo_disparo) - 0.5 * 9.81 * t**2

        # Calcular el valor máximo de x
        x_max = np.max(x)

        self.ax.set_xlim((0, x_max))
        self.ax.set_ylim((0, np.max(y)))

        line, = self.ax.plot([], [], color="red", marker="o")

        for i in range(len(t)):
            if self.option != "op_3":
                break
            line.set_data(x[:i+1], y[:i+1])
            self.root.after(0, self.canvas.draw)
               
    
def main():
    root = tk.Tk()
    server = Server(HOST, PORT, None)
    app = AppGUI(root, server)
    server.gui = app
    root.mainloop()

if __name__ == "__main__":
    main()