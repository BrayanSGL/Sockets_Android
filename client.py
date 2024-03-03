import socket

SERVER_IP = "192.168.20.26"  # Reemplaza con la IP del servidor
PORT = 6751

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_IP, PORT))

    while True:
        data = input("Ingrese los datos a enviar: ")
        client.send(data.encode("utf-8"))

        if data == "exit":
            break

    client.close()

if __name__ == "__main__":
    main()