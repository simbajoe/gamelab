from network import Network
from client import Client
from server import Server

if __name__ == '__main__':
    network = Network()
    server = Server()
    network.set_server(server)

    client1 = Client()
    client2 = Client()
    network.add_client(client1)
    network.add_client(client2)

    client1.connect()
    client1.send('Hello world!')
    client2.connect()
    client2.send('Hello too!')
    client1.send('Once again')

    print server.message_queue

