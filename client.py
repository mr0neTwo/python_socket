import socket
import threading


class Client:
    def __init__(self, server_host, server_port):
        self.server_host = server_host
        self.server_port = server_port
        self.nickname = ''
        self.encoding = 'ascii'
        self.batch = 1024
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_thread = None
        self.write_thread = None

    def start(self):
        self.set_nickname()
        self.connect()
        self.start_receive_thread()
        self.start_write_thread()

    def set_nickname(self):
        self.nickname = input("Write your nickname: ")

    def connect(self):
        self.client.connect((self.server_host, self.server_port))

    def start_receive_thread(self):
        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    def start_write_thread(self):
        self.write_thread = threading.Thread(target=self.write)
        self.write_thread.start()

    def receive(self):
        while True:
            try:
                message = self.client.recv(self.batch).decode(self.encoding)
                if message == 'NICK':
                    self.client.send(self.nickname.encode(self.encoding))
                else:
                    print(message)
            except:
                print('An error occurred!')
                self.client.close()
                break

    def write(self):
        while True:
            message = f'{self.nickname}: {input()}'
            self.client.send(message.encode(self.encoding))
