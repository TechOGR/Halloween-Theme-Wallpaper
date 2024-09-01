import socket
import threading

class TCPServer:
    def __init__(self, host='0.0.0.0', port=5000):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Servidor escuchando en {self.host}:{self.port}")

    def handle_client(self, client_socket):
        with client_socket:
            print("Cliente conectado")
            while True:
                try:
                    data = client_socket.recv(1024)
                    if not data:
                        break
                    print(f"Recibido: {data.decode('utf-8')}")
                    client_socket.sendall(data)  # Echo de los datos recibidos
                except ConnectionResetError:
                    print("Conexión con el cliente perdida")
                    break

    def start(self):
        print("Servidor iniciado")
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"Conexión aceptada de {addr}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_thread.start()

    def stop(self):
        self.server_socket.close()
        print("Servidor detenido")

