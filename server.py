import socket
import threading

from config import server_host, server_port


class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.encoding = 'ascii'
        self.batch = 1024
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.nicknames = []

    def run(self):
        self.server.bind((self.host, self.port))
        self.server.listen()
        self.receive()
        print("Server if listening...")

    def broadcast(self, message):
        for client in self.clients:
            client.send(message)

    def handle(self, client):
        while True:
            try:
                if not client._closed:
                    message = client.recv(self.batch)
                    self.broadcast(message)
            except Exception as error:
                self.remove_client(client)
                client.close()
                print(error)

    def remove_client(self, client):
        index = self.find_client_index(client)
        if index is not None:
            self.clients.pop(index)
            nickname = self.nicknames.pop(index)
            self.broadcast(f'{nickname} left!'.encode(self.encoding))

    def find_client_index(self, client):
        for index in range(len(self.clients)):
            if client.getpeername() == self.clients[index].getpeername():
                return index

    def receive(self):
        while True:
            client, address = self.server.accept()
            print(f"Connected with {address}")

            client.send('NICK'.encode(self.encoding))
            nickname = client.recv(self.batch).decode(self.encoding)
            self.nicknames.append(nickname)
            self.clients.append(client)

            print(f"Nickname is {nickname}")
            self.broadcast(f"{nickname} joined!".encode(self.encoding))
            client.send('Connected to server!'.encode(self.encoding))

            # Start Handling Thread For Client
            thread = threading.Thread(target=self.handle, args=(client,))
            thread.start()


if __name__ == '__main__':
    server = Server(server_host, server_port)
    server.run()

