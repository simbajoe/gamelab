from network import Network
from client import Client
from server import Server

class Simulation(object):

    def __init__(self, scenario):
        self.scenario = scenario

        self.network = Network()
        self.server = Server()
        self.network.set_server(self.server)

        self.clients = []

        for i in range(scenario.clients_number):
            client = Client()
            self.network.add_client(client)
            self.clients.append(client)

    def run(self):
        for event in self.scenario.events:
            print event
