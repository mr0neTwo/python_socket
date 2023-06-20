from client import Client
from config import server_host, server_port

client = Client(server_host, server_port)
client.start()