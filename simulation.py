from client import Client
from server import Server

class Simulation(object):
    MESSAGE_TYPE_CONNECT = 'connect'
    MESSAGE_TYPE_SEND = 'send'

    def __init__(self, scenario):
        self.scenario = scenario
        self.start = self.scenario.start
        self.end = self.scenario.end
        self.time = self.start

        self.server = Server()
        self.server.queue = []
        self.server.send = lambda client_id, message: self.server_send(client_id, message)
        self.server.receive = lambda: self.server_receive()
        self.server.get_time = lambda: self.scenario.props['local_time_start']['server'] + self.time

        self.clients = []
        for i in range(scenario.clients_number):
            client = Client()
            client.id = i
            client.queue = []
            client.connect = lambda: self.client_connect(client.id)
            client.send = lambda message: self.client_send(client.id, message)
            client.receive = lambda: self.client_receive()
            client.get_time = lambda: self.scenario.props['local_time_start']['client'][client_id] + self.time
            self.clients.append(client)

    def run(self):
        for time in range(self.start, self.end + 1):
            self.time = time
            yield self.model()

    def model(self):
        self.apply_events()
        self.server.mainloop()
        for client in self.clients:
            client.mainloop()
        return {
            'server': self.server.snapshot(),
            'client': [client.snapshot() for client in self.clients]
        }

    def apply_events(self):
        events = [None] * len(self.clients)
        if self.time in self.scenario.events:
            events = self.scenario.events[self.time]
        for client_id, event in enumerate(events):
            if not event:
                continue
            if event == '^':
                self.clients[client_id].connect()
                continue
            for key in event:
                event_type = 'keyup'
                if key.istitle():
                    event_type = 'keypress'
                method = getattr(self.clients[client_id], event_type)
                method(key.lower())

    def server_send(self, client_id, message):
        return self.clients[client_id].queue.append(message)

    def server_receive(self):
        queue = [x for x in self.server.queue]
        self.server.queue = []
        return queue

    def client_connect(self, client_id):
        return self.server.queue.append({'type': self.MESSAGE_TYPE_CONNECT, 'client': client_id})

    def client_send(self, client_id, message):
        return self.server.queue.append({'type': self.MESSAGE_TYPE_SEND, 'client': client_id, 'message': message})

    def client_receive(self, client_id):
        queue = [x for x in self.clients[client_id].queue]
        self.clients[client_id].queue = []
        return queue

